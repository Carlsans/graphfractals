# graphfractals: how it works, what worked, what did not

Written from the code and from the output left on disk: 19,292 PNGs and 9,585 logs in `Images/` (from 2024-04-05), 28,016 low-resolution PNGs with
10,146 logs in `lowres/unlabeled/`, and 31 class folders (Atypique, bacteroid, Dentelle, Floral, ...) holding a few dozen hand-sorted or autoencoder-sorted images each, used by the
[FractalAutoencoder](https://github.com/Carlsans/FractalAutoencoder) project. Statements marked *(inferred)* are conclusions from that evidence.

## The idea

Describe the *process* that makes a fractal as a **graph of nodes**, and let the process choose or evolve the formula by itself.

| Node | Class | Role |
|---|---|---|
| Initiator | `Initiator` | Set starting values (resolution, plane limits, thresholds). |
| Operator | `Operator` | Holds a list of Python assignments (`"z = z + c"`), evaluated with `eval` on the shared variables. |
| Evolutive operator | `OperatorEvolutiveFormula` | An operator whose formula is evolved between fractals. |
| Discriminator | `Discriminator` | A list of tests; each one can jump to another node. This makes loops and branches. |
| Iterator | `GraphIterator` | Walks all combinations of lists (functions, constants) in random order. |
| Outputer | `Outputer` | Saves the image and a log of chosen variables. |
| Edge filter | `Filter` | Renames variables along an edge (`"fractalresult as fractal1"`). |

`GraphDefinition.py` holds three graphs: `evolutivefractalgraph` (the one used for the 2024 runs), `singlefractalgraph`, `superposedfractalsgraph`.

### The evolutive graph

```
5 init values -> 10 init variables -> 20 evolutive formula, i+1 -> 30 test |z|^2 > 8 -> 40 mask newly escaped pixels
   -> 50 i < maxiter ? back to 20 : 60 grade -> 65 grade test
        65: grade < threshold -> back to 10 with a new formula candidate
            otherwise at preview resolution -> 67 switch to the final resolution -> 10 (same formula, bigger)
            at final resolution -> 70 save -> 75 raise the threshold by 0.01 (reset the formula when it passes 0.2) -> 10
```

The formula starts as `fn1(z,p1,p2)` (a tree of numpy functions with complex parameters) and is changed by one of six
random moves: switch a function, switch a variable, switch a parameter, add a branch, prune a branch, or cross with a formula from a pool
(`FormulaMutation`). Each candidate is rendered at 64x64 and graded; after `evoiterationsmax` candidates the best one is **kept** and becomes the base for the next round
(a hill climb with a population of one). A candidate above the threshold is rendered at full resolution and saved, and the formula is stored in a pool of 100
(`FormulaPool`, roulette selection) that later crossings draw from. The threshold starts at 0.13 and grows by 0.01 per accepted fractal up to 0.2, then the formula is reset.

The grade is the size of the PNG of the escape-iteration image divided by the number of pixels (`image_compression_based_information`).

## What worked

- **A simple grade.** PNG size per pixel stopped flat or noisy pictures, and the logs show accepted fractals between 0 and 0.24 (median about 0.09 over 2,000 logs).
  *(The log value is the grade of the full-resolution image, not the preview; the minimum of 0 is a log written for a discarded candidate.)*
- **Two resolutions.** Searching at 64x64 and re-rendering the winners made 28,883 images affordable.
- **Raising the bar over time.** The ratchet (0.13 to 0.2) avoids both an empty first phase and a plateau of mediocre images.
- **Tree mutation with pruning.** Trimming a branch and keeping the result only if the grade did not drop (`ispruning`) kept formulas from growing without limit.
- **A formula pool.** Crossing with earlier winners reused good sub-expressions.
- **Using the pictures to learn.** The low-resolution images fed a convolutional autoencoder with a classifier, trained on 31 named classes (Atypique, bacteroid, Dentelle, Floral, Hyperboid, mandala, ...).

## What did not work (or was left unfinished)

- **The graph engine is heavy for what it does.** The traversal in `FractalGraph.travelgraph` recurses, tracks "visitedby" lists for nodes with several parents, and never returns;
  a plain loop did the same job. Because values pass between nodes as Python dictionaries and operators are `eval` strings, errors show up far from their cause.
- **`FractalProcessing.py` ends with `exit()`** in its constructor, so `mandelbrottestcase` and its drawing are dead code.
- **`superposedfractalsgraph` cannot run.** It passes `(20, 60)` as the first arguments of `Discriminator` (which takes `sharedvalues` first) and calls a two-parameter function with one argument. The call was repaired in this repository.
- **`singlefractalgraph`** iterates over 20 x 20 x 8 x 10 x 10 = 320,000 combinations in random order. Most are not interesting, and its grade, closeness to a reference picture (`image_comparision_loss`), prefers pictures that resemble `compareme.jpg` rather than interesting ones.
- **`image_entropy`** (histogram entropy of four half-images) is computed but its result is only the last half's entropy. Compression replaced it.
- **Formula validity.** Many mutations produce formulas that raise or return a scalar; the code answers with `i = 1000000000` ("Bad evo function") to abort, which wastes evaluations.
- **A moving target.** The threshold changes during a run, so a grade of 0.15 is good early and mediocre late. The logs do not record the threshold of the moment except in `minimumfractalentropy`.
- **Pool files are pickles and conflicted.** Syncthing conflict copies (`pool.sync-conflict-*.pickle`) show several machines wrote the pool.
- **Windows batch helper** `opennpyfiles.bat` for `.npy` files whose saving is commented out.

## Lessons

1. A compression-based grade plus a rising threshold is a simple and effective generator of interesting escape-time pictures.
2. Keep a pool of past winners to cross with, but cap it and grade-weight it.
3. Search cheap (64x64), render expensive only for winners.
4. Do not let `eval` strings carry the whole program; the same loop in a few lines of Python is easier to debug and was easier to reuse in later projects (RewriteFractal, MatrixFractals).

## Running the original code

`GraphFractals/FractalProcessing.py` is the entry point, with the repository root on `PYTHONPATH`. It builds `evolutivefractalgraph()` and then calls `exit()`, so remove that line to
let the graph run (it never stops and saves into `GraphFractals/lowres/unlabeled/`). It needs `chime` (a sound on success) and `dill`.
