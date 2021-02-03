import random
from typing import Callable, Generator, List


def string_sampler(
    string_generator: Generator[str, None, None], ratio: float = 0.1, seed: int = 42
) -> Generator[str, None, None]:

    random.seed(seed)

    for string in string_generator:
        if random.random() <= ratio:
            yield string
        else:
            continue


def pretokenize_collator(
    string_generator: Generator[str, None, None],
    pretokenize_func: Callable[[str], List[str]],
) -> Generator[str, None, None]:

    for string in string_generator:
        for token in pretokenize_func(string):
            yield token
