# Features that exist in the code but are not part of the final workflow

| # | Feature | Where in the code | Why unused | In the GUI |
|---|---|---|---|---|
| 1 | Function-combination graph | `GraphDefinition.singlefractalgraph`, `GraphIterator` | Replaced by the evolutive formula | Run a graph > "Function combinations from lists" |
| 2 | Two superposed fractals | `GraphDefinition.superposedfractalsgraph` | Could not be built (constructor bug), never ran | Run a graph > "Two superposed fractals". The graph definition is repaired, and the run is a direct re-implementation with the arities fixed |
| 3 | Closeness-to-reference grade | `selectionsfunctions.image_comparision_loss` | Rewards looking like a given image | Grade list; a reference image can be chosen (default: the bundled `compareme.jpg`) |
| 4 | Histogram-entropy grade | `selectionsfunctions.image_entropy` | Replaced by compression | Grade list, and shown next to the compression grade in the Formula lab |
| 5 | Edge filters | `Edges/Filter.py` | Only the superposed graph used them | Used by the repaired superposed graph (shown in the graph picture) |
| 6 | Formula tree drawing | `FormulaTree.drawgraphformula` | Debug aid | Formula lab > Show formula tree |
| 7 | Formula pool | `FormulaPool.py` | Stored inside the source tree | Used by the evolutive run; stored in `~/.graphfractals/pool.pickle` instead of the repository |
| 8 | Graph drawing | `FractalGraph.drawGraph` | Needed `plt.show()` and a blocking window | Graph structure tab (node colours, labels, content table) |
| 9 | Plain Mandelbrot check | `FractalProcessing.mandelbrottestcase` | Dead code behind `exit()` | Formula lab: `z*z + c` renders it |
| 10 | Fractint formula file | `CustomFunctions/fractint.frm` | Reference only, never parsed | Not integrated: it is a text library of Fractint formulas and parsing them is a separate project |
| 11 | `.npy` viewer | `opennpyfilestoscreen.py`, `opennpyfiles.bat` | Saving of `.npy` is commented out | Not integrated |
