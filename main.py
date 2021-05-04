from tictactoe import *
from pathlib import Path
import json

if __name__ == "__main__":
    json.dump(grow_tree(), Path("./data.json").open("w"))
