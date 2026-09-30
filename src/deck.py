from datetime import datetime
from faulthandler import dump_traceback_later
from pathlib import Path
import json
from typing import Any, Union

from src.utils import safety_utils, file_utils


class MissingKey(ValueError):
    key: str
    object: Any
    def __init__(self, key, object):
        self.key = key
        self.object = object
class BucketDoesntExist(ValueError):
    bucket_index: int
    def __init__(self, bucket_index):
        self.bucket_index = bucket_index
class DeckNotInitialized(Exception):
    pass
class FileOpenError(OSError):
    error: Exception
    def __init__(self, e):
        self.error = e
class InvalidJson(ValueError):
    msg: str
    def __init__(self, msg):
        self.msg = msg

DeckLoadError = Union[
    MissingKey,
    BucketDoesntExist,
    DeckNotInitialized,
    FileOpenError,
    InvalidJson,
]


class Flashcard:
    path: Path
    async_study: bool

    def __init__(self, path: Path, async_study: bool = False):
        self.path = path
        self.async_study = async_study

class Bucket:
    size: int
    cards: list[Flashcard]

    def __init__(self, size: int):
        self.size = size
        self.cards = []

class Deck:
    last_changed: datetime
    buckets: list[Bucket]

    def __init__(self):
        self.last_changed = datetime.now()
        self.buckets = []

    @classmethod
    def try_load(cls, deck_directory: Path) -> Deck|DeckLoadError:
        deck_json_path = deck_directory / ".deck.json"
        if not deck_json_path.exists():
            return DeckNotInitialized()

        try:
            with open(deck_json_path, "r") as f:
                deck_json = json.load(f)
        except Exception as e:
            return FileOpenError(e)

        if not isinstance(deck_json, dict):
            return InvalidJson(f"JSON should have serialized into a dictionary. " \
                +"Instead it serialized into '{type(deck_json)}'")

        if "last updated" not in deck_json:
            return MissingKey("last updated", deck_json)
        if "bucket sizes" not in deck_json:
            return MissingKey("bucket sizes", deck_json)
        if "cards" not in deck_json:
            return MissingKey("cards", deck_json)


        deck = Deck()
        deck.last_changed = deck_json["last updated"]
        for size in deck_json["bucket sizes"]:
            deck.buckets.append(Bucket(size))
        for card_json in deck_json["cards"]:
            if "path" not in card_json:
                return MissingKey("path", card_json)
            if "bucket" not in card_json:
                return MissingKey("bucket", card_json)
            if "async study" not in card_json:
                return MissingKey("async study", card_json)

            bucket = card_json["bucket"]
            if 0 > bucket > len(deck.buckets):
                return BucketDoesntExist(bucket)

            deck.buckets[bucket].append(Flashcard(
                card_json["path"],
                card_json["async study"]
            ))

        return deck

    @classmethod
    def new_from_cli(cls, deck_directory: Path) -> Deck:
        deck = Deck()
        num_buckets = 1
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
        deck.buckets.append(Bucket(0))
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
                    deck.buckets.append(Bucket(inp))
                    break
                else:
                    safety_utils.assert_unreachable()

        for n, b in enumerate(deck.buckets):
            if n == 0: print("Bucket 0 is always reviewed")
            else: print(f"Bucket {n} can hold {b.size} cards before needing review")

        print("Scanning card files...")
        files = file_utils.scan_for_files(deck_directory)
        print(f"Found {len(files)} files")
        for i in files:
            deck.buckets[0].cards.append(Flashcard(Path(i.path)))

        return deck

    # def try_save(self, deck_directory: Path) -> None|FileOpenError:
    #     try:
    #         with open(deck_directory/".deck.json", "w") as f:
    #             json.dump()
