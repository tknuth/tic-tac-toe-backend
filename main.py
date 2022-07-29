from tictactoe import *
from pathlib import Path
import json

if __name__ == "__main__":
    with Path("./data.json").open("w") as f:
        json.dump(analyze_tree(grow_tree()), f)
