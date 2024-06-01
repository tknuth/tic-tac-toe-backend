import click
from tictactoe import *
from pathlib import Path
import json


@click.group
def cli():
    pass


@cli.command()
def export():
    with Path("./data.json").open("w") as f:
        json.dump(analyze_tree(grow_tree()), f)


@cli.command()
@click.option("--ai/--no-ai", default=False)
def play(ai):
    if ai:
        play_with_ai()
    else:
        play_without_ai()


if __name__ == "__main__":
    cli()
