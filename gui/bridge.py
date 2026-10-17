"""Glue between the PySide6 GUI and the graphfractals engine.

``FractalProcessing.py`` builds the graph and then calls ``exit()``; ``FractalGraph.processgraph`` loops forever and draws
with matplotlib. The GUI therefore keeps the engine's *nodes* (Initiator, Operator, OperatorEvolutiveFormula, Discriminator,
GraphIterator, Outputer), its *graph definitions* (``GraphDefinition``) and its *evolutive formula* code, and replaces only
the traversal loop with ``walk`` below, which yields events instead of printing and writing files.
"""
import contextlib
import copy
import io
import math
import sys
import types
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import numpy as np  # noqa: E402
import numpy.ma as ma  # noqa: E402
import networkx as nx  # noqa: E402
from matplotlib import colormaps  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def _install_shims():
    # chime plays a sound when a fractal is accepted; dill is only used by Outputer for an unused import.
    if "chime" not in sys.modules:
        try:
            import chime  # noqa: F401
        except ImportError:
            stub = types.ModuleType("chime")
            for name in ("success", "info", "warning", "error"):
                setattr(stub, name, lambda *a, **k: None)
            sys.modules["chime"] = stub
    try:
        import dill.source  # noqa: F401
    except ImportError:
        d = types.ModuleType("dill")
        s = types.ModuleType("dill.source")
        s.getsource = lambda *a, **k: ""
        d.source = s
        sys.modules.update({"dill": d, "dill.source": s})


_install_shims()

from GraphFractals.Configuration import Configuration  # noqa: E402
from GraphFractals.CustomFunctions import selectionsfunctions as sel  # noqa: E402
import GraphFractals.CustomFunctions.FractalFunctions as fn  # noqa: E402
from GraphFractals.CustomFunctions.fractaldomainfunctions import getComplexCoordinates  # noqa: E402
from GraphFractals.EvolutiveFormula.EvolutiveFunctionsManager import EvolutiveFunctionsManager  # noqa: E402
from GraphFractals.GraphDefinition import GraphDefinition  # noqa: E402
from GraphFractals.Nodes.GraphIterator import GraphIterator  # noqa: E402
import GraphFractals.Nodes.Operator as operator_module  # noqa: E402

GRADES = [
    ("image_compression_based_information", "PNG size per pixel (active)"),
    ("image_entropy", "Histogram entropy of four half-images (legacy)"),
    ("image_comparision_loss", "Closeness to a reference image (legacy)"),
]
GRAPHS = [("evolutivefractalgraph", "Evolving formula (active)"),
          ("singlefractalgraph", "Function combinations from lists (legacy)"),
          ("superposedfractalsgraph", "Two superposed fractals (legacy, repaired)")]
COLORMAPS = ["binary", "gist_earth", "nipy_spectral", "prism", "terrain", "twilight", "magma", "turbo"]


@contextlib.contextmanager
def quiet():
    with contextlib.redirect_stdout(io.StringIO()):
        yield


def make_conf(lowres=64, hires=256, maxiter=64, evoiterationsmax=40, entropy_start=0.13, entropy_stop=0.2, raise_by=0.01):
    conf = Configuration()
    conf.resolution = (hires, hires)
    conf.lowresfractalresolution = (lowres, lowres)
    conf.maxiter = maxiter
    conf.evoiterationsmax = evoiterationsmax
    conf.minimumfractalentropystart = entropy_start
    conf.maximumfractalentropystop = entropy_stop
    conf.entropyraise = raise_by
    conf.drawgraph = False
    return conf


class _FP:
    """What GraphDefinition needs from FractalProcessing."""

    def __init__(self, conf):
        self.conf = conf

    def getComplexCoordinates(self):
        n, m = self.conf.resolution
        real = np.linspace(self.conf.limitreal[0], self.conf.limitreal[1], n)
        imag = np.linspace(self.conf.limitimag[0], self.conf.limitimag[1], m)
        coords = np.ones([n, m], dtype=self.conf.dtype) * real + np.ones([n, m]) * imag.reshape(1, -1).T * 1j
        return ma.array(coords, mask=np.zeros_like(coords))


def set_reference_image(path):
    """Legacy 'closeness to a reference image' grade: use this image instead of the missing compareme.jpg."""
    from PIL import Image
    img = np.asarray(Image.open(path).convert("L"), dtype=np.float64) / 255.0

    def loss(fractal):
        if np.min(fractal) == np.max(fractal):
            return 0
        small = np.asarray(Image.fromarray((img * 255).astype(np.uint8)).resize(fractal.shape[::-1])) / 255.0
        normalized = (fractal - np.min(fractal)) / (np.max(fractal) - np.min(fractal))
        return 1 - float(np.mean(np.abs(small - normalized)))
    operator_module.image_comparision_loss = loss


def set_grade_function(graph, name):
    """The 'Entropy Calculator' operator holds the grade as source text; swap the function name."""
    for node, data in graph.nodes(data=True):
        obj = data['object']
        if obj.getName() == "Entropy Calculator":
            obj.functionlist = [f"fractalentropy = {name}(fractalresult)" if f.startswith("fractalentropy") else f
                                for f in obj.functionlist]


POOL_PATH = Path.home() / ".graphfractals" / "pool.pickle"


def _patch_pool():
    """FormulaPool reads and writes GraphFractals/EvolutiveFormula/pool/pool.pickle inside the source tree.
    Keep the pool in the user's home instead so that running the GUI never touches the repository."""
    import os
    import pickle
    from GraphFractals.EvolutiveFormula import FormulaPool as fp_module
    cls = fp_module.FormulaPool
    if getattr(cls, "_gui_patched", False):
        return

    def init(self):
        self.minimumgrade, self.maxpoolsize, self.pool = 0.2, 100, []
        self.poolfilepath = str(POOL_PATH)
        if os.path.isfile(self.poolfilepath):
            try:
                self.loadpool()
            except Exception:
                self.pool = []

    def savepool(self):
        os.makedirs(os.path.dirname(self.poolfilepath), exist_ok=True)
        with open(self.poolfilepath, "wb") as handle:
            pickle.dump(self.pool, handle, protocol=pickle.HIGHEST_PROTOCOL)
    cls.__init__, cls.savepool, cls._gui_patched = init, savepool, True


def build_graph(kind, conf):
    _patch_pool()
    with quiet():
        definition = GraphDefinition(_FP(conf))
        graph, start = getattr(definition, kind)()
    return graph, start


def node_summary(graph):
    rows = []
    for node in sorted(graph.nodes):
        obj = graph.nodes[node]['object']
        rows.append((node, type(obj).__name__, obj.getName(), obj.getProperties().strip()))
    return rows


def draw_graph(graph, width=900, height=520):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(width / 100, height / 100), dpi=100)
    pos = nx.circular_layout(graph)
    colors = [graph.nodes[n]['object'].getColor() for n in graph.nodes]
    labels = {n: f"{n}\n{graph.nodes[n]['object'].getName()}" for n in graph.nodes}
    nx.draw_networkx_nodes(graph, pos, node_color=colors, node_size=900, alpha=.85)
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=6)
    nx.draw_networkx_edges(graph, pos, arrowsize=14, connectionstyle="arc3,rad=0.12", node_size=900)
    plt.axis("off")
    fig.tight_layout()
    fig.canvas.draw()
    rgb = np.asarray(fig.canvas.buffer_rgba())[..., :3].copy()
    plt.close(fig)
    return rgb


def colorize(field, cmap="binary"):
    field = np.ma.filled(np.ma.asarray(field, dtype=float), np.nan)
    finite = field[np.isfinite(field)]
    if finite.size == 0:
        return np.zeros((*field.shape, 3), np.uint8)
    lo, hi = finite.min(), finite.max()
    norm = np.nan_to_num((field - lo) / (hi - lo + 1e-9))
    return np.ascontiguousarray((colormaps.get_cmap(cmap)(norm)[..., :3] * 255).astype(np.uint8))


# ---------------------------------------------------------------- graph walker
def walk(graph, start, on_event, job=None, max_steps=10_000_000):
    """Execute the graph like FractalGraph.travelgraph, without the recursion and the infinite loop.

    on_event(node_id, node_object, values) is called after every node is applied.
    The walk ends when a node without successor is reached and no GraphIterator has combinations left.
    """
    node, message, steps = start, None, 0
    iterators = [n for n in graph.nodes if isinstance(graph.nodes[n]['object'], GraphIterator)]
    while steps < max_steps:
        if job is not None and job.should_stop():
            return
        obj = graph.nodes[node]['object']
        with quiet():
            obj.processNode(message)
            if isinstance(obj, GraphIterator) and obj.iterationended:
                return
            answer = obj.applyNode()
        on_event(node, obj, getattr(obj, 'values', None) or {})
        message, steps = answer, steps + 1
        choice = answer['nextnodechoice']
        if choice is None:
            return
        if choice != -1:
            node = choice
            continue
        successors = list(graph.successors(node))
        if successors:
            node = successors[0]
        elif iterators and not all(graph.nodes[i]['object'].iterationended for i in iterators):
            node, message = start, None
        else:
            return


def run_graph(kind, conf, grade="image_compression_based_information", reference=None, job=None, log=print,
              on_candidate=None, on_accept=None):
    """Run one of the engine's graphs. Callbacks get (fractalresult array, info dict)."""
    if kind == "superposedfractalsgraph":
        return run_superposed(conf, job, log, on_candidate, on_accept)
    if grade == "image_comparision_loss":
        # The engine's version writes comparemeresized.jpg into its own source folder; use ours instead.
        set_reference_image(reference or str(REPO / "GraphFractals" / "CustomFunctions" / "compareme.jpg"))
    graph, start = build_graph(kind, conf)
    set_grade_function(graph, grade)
    for n, data in graph.nodes(data=True):
        if type(data['object']).__name__ == "Outputer":
            data['object'].savetodisk = False
            data['object'].show = False
            data['object'].savelog = lambda *a, **k: None   # the engine writes a .log next to every output
    counters = {"candidates": 0, "accepted": 0}

    def info(values):
        d = {k: values.get(k) for k in ("fractalentropy", "minimumfractalentropy", "evolutivefunction", "fractalresolution",
                                        "evoiterations", "npfunc_parameter", "npfunc2_parameter", "npfunc3_parameter")}
        for k in ("p1", "p2"):
            if k in values:
                d[k] = values[k]
        return d

    def on_event(node, obj, values):
        name = obj.getName()
        if name == "Entropy Calculator" and 'fractalresult' in values:
            counters["candidates"] += 1
            if on_candidate:
                on_candidate(np.ma.filled(values['fractalresult'], -1), info(values))
        elif type(obj).__name__ == "Outputer" and 'fractalresult' in values:
            counters["accepted"] += 1
            if on_accept:
                on_accept(np.ma.filled(values['fractalresult'], -1), info(values))
            log(f"accepted #{counters['accepted']}: grade {values.get('fractalentropy')}")

    walk(graph, start, on_event, job)
    return counters


# ---------------------------------------------------------------- repaired superposed graph
def _wrap(name):
    """Turn 'fn.zmpone' / 'ma.cos' into a callable with the arity GraphIterator would give it."""
    return eval(name, {"fn": fn, "ma": ma, "np": np})


def run_superposed(conf, job=None, log=print, on_candidate=None, on_accept=None, threshold=0.15, seed=None):
    """Two escape-time fractals with random functions, summed (GraphDefinition.superposedfractalsgraph).

    The original cannot run: it passes (20, 60) as the first arguments of Discriminator and calls the two-parameter
    function npfunc3 with one argument. Here fractal 1 is z = f3(f1(z*z), c) and fractal 2 is z = f2(z*z) + c, as intended.
    """
    import random
    rng = random.Random(seed)
    definition = GraphDefinition(_FP(conf))
    ones, twos = definition.funclist, definition.funclisttwoparam
    counters = {"candidates": 0, "accepted": 0}
    while job is None or not job.should_stop():
        f1, f2, f3 = rng.choice(ones), rng.choice(ones), rng.choice(twos)
        try:
            a = _escape(lambda z, c: _wrap(f3)(_wrap(f1)(z * z), c), conf.lowresfractalresolution, conf)
            b = _escape(lambda z, c: _wrap(f2)(z * z) + c, conf.lowresfractalresolution, conf)
        except Exception:
            continue
        low = a + b
        counters["candidates"] += 1
        grade = _grade(low, "image_compression_based_information")
        meta = {"fractalentropy": grade, "npfunc_parameter": f1, "npfunc2_parameter": f2, "npfunc3_parameter": f3}
        if on_candidate:
            on_candidate(low, meta)
        if grade is not None and not math.isnan(grade) and grade >= threshold:
            a = _escape(lambda z, c: _wrap(f3)(_wrap(f1)(z * z), c), conf.resolution, conf)
            b = _escape(lambda z, c: _wrap(f2)(z * z) + c, conf.resolution, conf)
            counters["accepted"] += 1
            if on_accept:
                on_accept(a + b, meta)
            log(f"accepted #{counters['accepted']}: {f1}, {f2}, {f3}")
    return counters


def _escape(step, resolution, conf, bailout=4):
    c = getComplexCoordinates(resolution, conf.limitreal, conf.limitimag, conf.dtype)
    z = ma.masked_array(copy.deepcopy(c), mask=np.zeros_like(c))
    hasdropped = ma.ones_like(c, dtype=np.bool_)
    result = np.zeros_like(c, dtype=np.int32) - 1
    with np.errstate(all="ignore"):
        for i in range(1, conf.maxiter + 1):
            z = step(z, c)
            dropout = (z.real * z.real) + (z.imag * z.imag) > bailout
            newdrop = np.all([dropout, hasdropped], axis=0)
            z[newdrop] = ma.masked
            result[newdrop] = i
            hasdropped = dropout
    return result


def _grade(field, name):
    func = {"image_compression_based_information": sel.image_compression_based_information,
            "image_entropy": sel.image_entropy}.get(name, sel.image_compression_based_information)
    with quiet():
        return float(func(field))


# ---------------------------------------------------------------- formula lab
def render_formula(formula, resolution=(256, 256), maxiter=64, bailout=8, limit=2.0, conf=None):
    """Escape-time picture of a formula written like the engine's evolved ones, e.g.
    ``evo.add(evo.multiply(z, z), c)`` or ``evo.sin(z) + c``. Variables: z, c; functions: evo.*, fn.*, np.*."""
    conf = conf or make_conf(hires=resolution[0], maxiter=maxiter)
    conf.limitreal = conf.limitimag = [-limit, limit]
    manager = EvolutiveFunctionsManager()
    env = {"np": np, "ma": ma, "evo": manager, "fn": fn}
    code = compile(formula, "<formula>", "eval")
    return _escape(lambda z, c: eval(code, env, {"z": z, "c": c}), resolution, conf, bailout)


def formula_graph_picture(formula):
    from GraphFractals.EvolutiveFormula.FormulaTree import FormulaTree
    import matplotlib.pyplot as plt
    with quiet():
        graph = FormulaTree().formulatograph(formula)
    fig = plt.figure(figsize=(7, 4.5), dpi=100)
    nx.draw(graph, with_labels=True, node_size=500, font_size=7)
    fig.canvas.draw()
    rgb = np.asarray(fig.canvas.buffer_rgba())[..., :3].copy()
    plt.close(fig)
    return rgb


def grade_image(field, name="image_compression_based_information"):
    return _grade(field, name)
