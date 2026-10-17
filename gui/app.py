"""graphfractals GUI. Run from the repository root:  python -m gui.app"""
import sys
import threading
import traceback

import numpy as np
from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFileDialog, QFormLayout, QGroupBox, QHBoxLayout,
                               QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QPlainTextEdit, QPushButton,
                               QSpinBox, QTableWidget, QTableWidgetItem, QTabWidget, QVBoxLayout, QWidget)

from gui import bridge  # noqa: E402


class Job(QThread):
    log = Signal(str)
    candidate = Signal(object, object)
    accepted = Signal(object, object)
    finished_ok = Signal(object)
    failed = Signal(str)

    def __init__(self, fn):
        super().__init__()
        self.fn, self._stop = fn, threading.Event()

    def should_stop(self):
        return self._stop.is_set()

    def stop(self):
        self._stop.set()

    def run(self):
        try:
            self.finished_ok.emit(self.fn(self))
        except Exception:
            self.failed.emit(traceback.format_exc())


def to_pixmap(rgb, width=None):
    rgb = np.ascontiguousarray(rgb)
    h, w, _ = rgb.shape
    pix = QPixmap.fromImage(QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888).copy())
    return pix.scaledToWidth(width, Qt.SmoothTransformation) if width else pix


class ImageView(QLabel):
    def __init__(self, size=400):
        super().__init__("no image")
        self.setMinimumSize(size, size // 2)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background:#111;color:#888")
        self.rgb = None

    def show_rgb(self, rgb):
        self.rgb = rgb
        self.setPixmap(to_pixmap(rgb, max(min(self.width(), 900) - 4, 100)))


class LogBox(QPlainTextEdit):
    def __init__(self, height=90):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumBlockCount(300)
        self.setMaximumHeight(height)

    def add(self, text):
        self.appendPlainText(text)


class RunTab(QWidget):
    def __init__(self):
        super().__init__()
        self.job, self.accepted_items = None, []
        self.kind = QComboBox()
        for key, label in bridge.GRAPHS:
            self.kind.addItem(label, key)
        self.grade = QComboBox()
        for key, label in bridge.GRADES:
            self.grade.addItem(label, key)
        self.reference = QLineEdit(); self.reference.setPlaceholderText("reference image for the closeness grade (legacy)")
        b_ref = QPushButton("..."); b_ref.clicked.connect(self.pick_ref)
        self.low = self._spin(16, 256, 48); self.high = self._spin(32, 2048, 256)
        self.maxiter = self._spin(10, 1000, 64); self.evomax = self._spin(2, 1000, 40)
        self.ent0 = self._dspin(0, 1, 0.13); self.ent1 = self._dspin(0, 1, 0.20); self.entup = self._dspin(0, 1, 0.01)
        self.cmap = QComboBox(); self.cmap.addItems(bridge.COLORMAPS)
        self.cmap.currentTextChanged.connect(lambda _: self.recolor())
        self.start = QPushButton("Start"); self.stop = QPushButton("Stop")
        self.start.clicked.connect(self.begin); self.stop.clicked.connect(self.end)
        b_save = QPushButton("Save selected PNG"); b_save.clicked.connect(self.save)
        self.cand_view = ImageView(300); self.acc_view = ImageView(300)
        self.info = QLabel(""); self.info.setWordWrap(True)
        self.gallery = QListWidget(); self.gallery.setViewMode(QListWidget.IconMode); self.gallery.setIconSize(QPixmap(96, 96).size())
        self.gallery.setResizeMode(QListWidget.Adjust); self.gallery.setMaximumHeight(140)
        self.gallery.currentRowChanged.connect(self.select)
        self.log = LogBox()
        self.current_field, self.field_data = None, []
        form = QFormLayout()
        form.addRow("Graph", self.kind); form.addRow("Grade", self.grade)
        form.addRow("Reference image", self._row(self.reference, b_ref))
        form.addRow("Preview resolution", self.low); form.addRow("Final resolution", self.high); form.addRow("Max iterations", self.maxiter)
        form.addRow("Steps per formula before choosing the best", self.evomax)
        form.addRow("Grade threshold: start / stop / step", self._row(self.ent0, self.ent1, self.entup))
        form.addRow("Colormap", self.cmap)
        row = QHBoxLayout(); row.addWidget(self.start); row.addWidget(self.stop); row.addWidget(b_save)
        left = QVBoxLayout(); left.addLayout(form); left.addLayout(row); left.addWidget(self.info)
        views = QHBoxLayout()
        v1 = QVBoxLayout(); v1.addWidget(QLabel("Candidate being tested")); v1.addWidget(self.cand_view, 1)
        v2 = QVBoxLayout(); v2.addWidget(QLabel("Accepted fractals")); v2.addWidget(self.acc_view, 1)
        views.addLayout(v1, 1); views.addLayout(v2, 1)
        right = QVBoxLayout(); right.addLayout(views); right.addWidget(self.gallery)
        top = QHBoxLayout(); top.addLayout(left, 1); top.addLayout(right, 3)
        lay = QVBoxLayout(self); lay.addLayout(top); lay.addWidget(self.log)

    @staticmethod
    def _spin(lo, hi, v):
        w = QSpinBox(); w.setRange(lo, hi); w.setValue(v); return w

    @staticmethod
    def _dspin(lo, hi, v):
        w = QDoubleSpinBox(); w.setRange(lo, hi); w.setDecimals(3); w.setSingleStep(.01); w.setValue(v); return w

    @staticmethod
    def _row(*widgets):
        w = QWidget(); l = QHBoxLayout(w); l.setContentsMargins(0, 0, 0, 0)
        for x in widgets:
            l.addWidget(x)
        return w

    def pick_ref(self):
        path, _ = QFileDialog.getOpenFileName(self, "Reference image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.reference.setText(path)

    def begin(self):
        if self.job is not None and self.job.isRunning():
            return
        conf = bridge.make_conf(self.low.value(), self.high.value(), self.maxiter.value(), self.evomax.value(),
                                self.ent0.value(), self.ent1.value(), self.entup.value())
        kind, grade, ref = self.kind.currentData(), self.grade.currentData(), self.reference.text() or None
        self.job = Job(lambda job: bridge.run_graph(kind, conf, grade, ref, job, job.log.emit,
                                                    lambda a, i: job.candidate.emit(a, i), lambda a, i: job.accepted.emit(a, i)))
        self.job.log.connect(self.log.add)
        self.job.candidate.connect(self.on_candidate)
        self.job.accepted.connect(self.on_accepted)
        self.job.failed.connect(lambda tb: self.log.add(tb.strip().splitlines()[-1]))
        self.job.finished.connect(lambda: (self.start.setEnabled(True), self.log.add("stopped")))
        self.start.setEnabled(False)
        self.job.start()

    def end(self):
        if self.job is not None:
            self.job.stop()

    def describe(self, info):
        parts = []
        for k in ("fractalentropy", "minimumfractalentropy"):
            if info.get(k) is not None:
                parts.append(f"{k} = {info[k]:.4f}")
        for k in ("evolutivefunction", "npfunc_parameter", "npfunc2_parameter", "npfunc3_parameter"):
            if info.get(k):
                parts.append(f"{k} = {info[k]}")
        return "\n".join(parts)

    def on_candidate(self, field, info):
        self.cand_view.show_rgb(bridge.colorize(field, self.cmap.currentText()))
        self.info.setText(self.describe(info))

    def on_accepted(self, field, info):
        self.field_data.append((field, info))
        rgb = bridge.colorize(field, self.cmap.currentText())
        item = QListWidgetItem(QIcon(to_pixmap(rgb).scaled(96, 96)), f"{info.get('fractalentropy') or 0:.3f}")
        self.gallery.addItem(item)
        self.gallery.setCurrentRow(self.gallery.count() - 1)

    def select(self, row):
        if 0 <= row < len(self.field_data):
            field, info = self.field_data[row]
            self.acc_view.show_rgb(bridge.colorize(field, self.cmap.currentText()))
            self.info.setText(self.describe(info))

    def recolor(self):
        for i, (field, info) in enumerate(self.field_data):
            self.gallery.item(i).setIcon(QIcon(to_pixmap(bridge.colorize(field, self.cmap.currentText())).scaled(96, 96)))
        self.select(self.gallery.currentRow())

    def save(self):
        if self.acc_view.rgb is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save", "fractal.png", "PNG (*.png)")
        if path:
            from matplotlib import pyplot as plt
            plt.imsave(path, self.acc_view.rgb)


class GraphTab(QWidget):
    def __init__(self):
        super().__init__()
        self.kind = QComboBox()
        for key, label in bridge.GRAPHS:
            self.kind.addItem(label, key)
        b = QPushButton("Show graph"); b.clicked.connect(self.show_graph)
        self.view = ImageView(500)
        self.table = QTableWidget(0, 4); self.table.setHorizontalHeaderLabels(["id", "type", "name", "content"])
        self.table.horizontalHeader().setStretchLastSection(True)
        lay = QVBoxLayout(self)
        row = QHBoxLayout(); row.addWidget(self.kind, 1); row.addWidget(b); lay.addLayout(row)
        lay.addWidget(QLabel("Nodes are coloured by type: blue initiator, green operator, red discriminator, yellow iterator, pink output. "
                             "Each operator holds Python expressions that are evaluated on the shared variables."))
        lay.addWidget(self.view, 2); lay.addWidget(self.table, 1)

    def show_graph(self):
        conf = bridge.make_conf()
        graph, _ = bridge.build_graph(self.kind.currentData(), conf)
        self.view.show_rgb(bridge.draw_graph(graph))
        rows = bridge.node_summary(graph)
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(value).replace("\n", "  |  ")))


class FormulaTab(QWidget):
    def __init__(self):
        super().__init__()
        self.formula = QLineEdit("evo.add(evo.multiply(z, z), c)")
        self.formula.setToolTip("z and c are complex arrays. Functions: evo.add/subtract/multiply/divide/sin/cos/tan/arcsin/arccos/arctan/"
                                "naturallog/parallelofz, fn.* (zmpone, zbyz, flip, inverse, parallel...), np.*, ma.*")
        self.res = QSpinBox(); self.res.setRange(32, 2048); self.res.setValue(256)
        self.maxiter = QSpinBox(); self.maxiter.setRange(5, 2000); self.maxiter.setValue(64)
        self.limit = QDoubleSpinBox(); self.limit.setRange(0.01, 100); self.limit.setValue(2.0)
        self.bail = QDoubleSpinBox(); self.bail.setRange(1, 1e6); self.bail.setValue(8)
        self.cmap = QComboBox(); self.cmap.addItems(bridge.COLORMAPS)
        self.grade = QLabel("")
        b = QPushButton("Render"); b.clicked.connect(self.render)
        bt = QPushButton("Show formula tree"); bt.clicked.connect(self.tree)
        self.view = ImageView(400); self.tree_view = ImageView(300); self.log = LogBox(60)
        form = QFormLayout()
        form.addRow("Formula", self.formula); form.addRow("Resolution", self.res); form.addRow("Iterations", self.maxiter)
        form.addRow("Half-width of the plane", self.limit); form.addRow("Bailout (|z|^2 >)", self.bail); form.addRow("Colormap", self.cmap)
        row = QHBoxLayout(); row.addWidget(b); row.addWidget(bt)
        left = QVBoxLayout(); left.addLayout(form); left.addLayout(row); left.addWidget(self.grade); left.addWidget(self.tree_view, 1)
        top = QHBoxLayout(); top.addLayout(left, 1); top.addWidget(self.view, 2)
        lay = QVBoxLayout(self); lay.addLayout(top); lay.addWidget(self.log)

    def render(self):
        try:
            field = bridge.render_formula(self.formula.text(), (self.res.value(),) * 2, self.maxiter.value(), self.bail.value(),
                                          self.limit.value())
        except Exception as exc:
            self.log.add(f"{type(exc).__name__}: {exc}"); return
        self.view.show_rgb(bridge.colorize(field, self.cmap.currentText()))
        try:
            self.grade.setText(f"PNG size per pixel: {bridge.grade_image(field):.4f}   histogram entropy: "
                               f"{bridge.grade_image(field, 'image_entropy'):.4f}")
        except Exception as exc:
            self.grade.setText(str(exc))

    def tree(self):
        try:
            self.tree_view.show_rgb(bridge.formula_graph_picture(self.formula.text().replace("evo.", "fn_").replace("fn.", "fn_")))
        except Exception as exc:
            self.log.add(f"tree: {type(exc).__name__}: {exc}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("graphfractals")
        tabs = QTabWidget()
        self.run_tab, self.graph_tab, self.formula_tab = RunTab(), GraphTab(), FormulaTab()
        for w, name in ((self.run_tab, "Run a graph"), (self.graph_tab, "Graph structure"), (self.formula_tab, "Formula lab")):
            tabs.addTab(w, name)
        self.setCentralWidget(tabs)
        self.resize(1250, 800)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
