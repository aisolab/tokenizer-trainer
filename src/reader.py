import re
from pathlib import Path
from typing import Generator, Union

CHAR_PATTERN = re.compile(r"\S+")


def read_corpus(filepath: Union[Path, str]) -> Generator[str, None, None]:
    io = open(filepath, mode="r", encoding="utf-8")

    while True:
        try:
            string = next(io)
            if CHAR_PATTERN.match(string):
                yield string.strip()
            else:
                continue
        except StopIteration:
            break
    io.close()


def read_corpora(version_dir_path: Union[Path, str]) -> Generator[str, None, None]:
    if isinstance(version_dir_path, str):
        version_dir_path = Path(version_dir_path)

    list_of_filepath = []
    for path in version_dir_path.iterdir():
        if path.is_dir():
            list_of_filepath.extend(list(path.glob("*.txt")))
        elif path.suffix == ".txt":
            list_of_filepath.append(path)

    list_of_string_generator = [read_corpus(filepath) for filepath in list_of_filepath]

    for string_generator in list_of_string_generator:
        for string in string_generator:
            yield string
