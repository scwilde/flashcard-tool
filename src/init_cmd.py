import typer
from pathlib import Path
from typing import Annotated
from datetime import datetime, timezone
import json

from utils import safety_utils, file_utils

cmd = typer.Typer()

@cmd.command()
def init(deck_directory: Annotated[Path, typer.Argument(
    exists=True,
    file_okay=False,
    dir_okay=True,
    resolve_path=True,
    help="Optional path to deck directory. If not specified then cwd is used."
)] = Path.cwd()) -> None:
    """Initialize a directory of files into a new flashcard deck.

    The name of the file will be the front of the card and the contents of the file will be the back.
    Only text files and PNG images are supported."""

    deck_json = deck_directory / ".deck.json"
    if deck_json.exists():
        print(f"Deck at '{deck_directory}' is already initialized")

    else:
        deck = {
            "last update": datetime.now().timestamp(),
            "buckets": [],
            "cards": []
        }

        num_buckets: int = 1;
        print(f"Initializing new flashcard deck at '{deck_directory}'...")
        while True:
            inp = safety_utils.try_to_int(input("How many buckets would you like to add?[1] ") or "1")
            if isinstance(inp, ValueError):
                print(f"Please enter an integer")
            elif isinstance(inp, int) and inp < 1:
                print(f"There must be at least 1 bucket")
            elif isinstance(inp, int) and inp >= 1:
                num_buckets = inp
                break
            else:
                safety_utils.assert_unreachable()

        print("Bucket 0 always has a capacity of 0 (always used in reviews)")
        deck["buckets"].append(0)
        for i in range(1, num_buckets):
            while True:
                inp = safety_utils.try_to_int(input(
                    f"How many cards should fit in Bucket {i}?\n" \
                    + "(Bucket will be added to review if it has >n cards inside of it) "
                ))
                if isinstance(inp, ValueError):
                    print("Please enter and integer")
                elif isinstance(inp, int) and inp < 0:
                    print("A bucket cannot have a negative capacity")
                elif isinstance(inp, int) and inp > 0:
                    deck["buckets"].append(inp)
                    break
                else:
                    safety_utils.assert_unreachable()
        for n, b in enumerate(deck["buckets"]):
            if n == 0: print("Bucket 0 is always reviewed")
            else: print(f"Bucket {n} can hold {b} cards before needing review")

        print("Scanning card files...")
        files = file_utils.scan_for_files(deck_directory)
        print(f"Found {len(files)} files")
        for i in files:
            deck["cards"].append({
                "path": i.path,
                "bucket": 0,
                "async study": False,
            })

        with open(deck_json, "w") as f:
            f.write(json.dumps(deck, indent="    "))
