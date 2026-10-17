import os
import sys
from pathlib import Path
import numpy as np
#from ManualFractalExploration.ManualFractalExploration import ExplorationWindow


def main():
    path = sys.argv[1]
    filename = Path(path).stem
    array = np.load(path)
    np.set_printoptions(threshold=sys.maxsize)
    print(array)
    input()

if __name__ == "__main__":
    main()