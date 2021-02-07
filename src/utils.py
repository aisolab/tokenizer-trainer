import itertools
import logging
import re
from pathlib import Path
from typing import Generator, List, Union

import datasets

WHITESPACE_PATTERN = re.compile(r"\s+")


def get_logger(process_name: str) -> logging.Logger:
    formatter = logging.Formatter(
        fmt="[%(asctime)-10s] (line: %(lineno)d) %(name)s:%(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename="debug.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(process_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def extract_filepath_from_dir(
    dirpath: Union[Path, str], ext: str = "txt"
) -> Union[List[str], List[Path]]:
    if isinstance(dirpath, str):
        dirpath = Path(dirpath)

    list_of_filepath = []
    for filepath in dirpath.iterdir():
        if filepath.is_dir():
            list_of_filepath.extend(list(filepath.glob("*.txt")))
        elif filepath.suffix == f".{ext}":
            list_of_filepath.append(filepath)
    return list_of_filepath


def read_corpus(
    filepath: Union[Path, str], skip_whitespace_line: bool = True
) -> Generator[str, None, None]:
    io = open(filepath, mode="r", encoding="utf-8")

    if skip_whitespace_line:
        while True:
            try:
                string = next(io)
                if WHITESPACE_PATTERN.match(string):
                    continue
                yield string.strip()
            except StopIteration:
                break
    else:
        while True:
            try:
                string = next(io)
                yield string.strip() if len(string) != 1 else string
            except StopIteration:
                break

    io.close()


def read_corpora(
    version_dir_path: Union[Path, str],
    ext: str = "txt",
    skip_whitespace_line=True,
) -> Generator[str, None, None]:
    list_of_filepath = extract_filepath_from_dir(version_dir_path, ext)

    list_of_string_generator = itertools.chain(
        read_corpus(filepath, skip_whitespace_line) for filepath in list_of_filepath
    )

    for string_generator in list_of_string_generator:
        for string in string_generator:
            yield string


# TODO: token generator에서 배치로 내보내는 기능 구현
def convert_to_token_generator(
    preprocessed_corpus: datasets.arrow_dataset.Dataset,
    key: str = "text",
) -> Generator[str, None, None]:
    preprocessed_corpus_iterator = iter(preprocessed_corpus)

    for item in preprocessed_corpus_iterator:
        list_of_tokens = item[key]
        yield from list_of_tokens
