# graphfractals

Escape-time fractals produced by a **graph of processing nodes**. The main graph evolves a numpy formula by random mutation, grades each candidate by how poorly its picture compresses,
and keeps raising the bar.

- How it works, what worked and what did not: [docs/PROJECT.md](docs/PROJECT.md)
- Features that were tried and dropped: [docs/UNUSED_FEATURES.md](docs/UNUSED_FEATURES.md)

## GUI

```
pip install -r requirements-gui.txt
python -m gui.app
```

- **Run a graph**: pick one of the three graphs and a grade, watch the candidates, collect accepted fractals, save them.
- **Graph structure**: draw a graph and list the expressions held by its nodes.
- **Formula lab**: render any formula (`evo.add(evo.multiply(z, z), c)`), see both grades and the formula tree.

The evolved formula pool is kept in `~/.graphfractals/pool.pickle`. Pools are Python pickles: only load your own.

## Original scripts

`GraphFractals/FractalProcessing.py` (see the project notes: its constructor ends with `exit()`).

## License

[PolyForm Noncommercial 1.0.0](LICENSE). Personal, research and hobby use are allowed; commercial use is not.

## Launch the GUI

Linux: `./run.sh`  
Windows: `run_win.bat`

The first run creates a `.venv` and installs `requirements-gui.txt`; later runs start immediately.
