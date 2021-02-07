from typing import Dict, List

from konlpy.tag import Mecab
from kss import split_sentences


class SentenceSplitter:
    def __init__(self, lang: str = "ko") -> None:
        self._split = split_sentences
        if lang == "ko":
            self._split = split_sentences
        # TODO: 다른 언어의 문장 분리를 지원

    def process(self, example: Dict[str, List[str]]) -> Dict[str, List[str]]:
        example["text"] = self.split(example["text"])
        return example

    def split(self, string: str) -> List[str]:
        return self._split(string)


class MorphemeSplitter:
    def __init__(self, lang: str = "ko") -> None:
        self._split = Mecab().morphs
        if lang == "ko":
            self._split = Mecab().morphs
        # TODO: 다른 언어에 대해서 형태소 분석을 지원

    def split(self, string: str) -> List[str]:
        return self._split(string)

    def process(self, example: Dict[str, List[str]]) -> Dict[str, List[str]]:
        if isinstance(example["text"], list):
            list_of_tokens = []
            for sentence in example["text"]:
                list_of_tokens.extend(self.split(sentence))
            example["text"] = list_of_tokens
            return example
        example["text"] = self.split(example["text"])
        return example


class SpaceSplitter:
    def __init__(self) -> None:
        pass

    def split(self, string: str) -> List[str]:
        return string.split(" ")

    def process(self, example: Dict[str, List[str]]) -> Dict[str, List[str]]:
        if isinstance(example["text"], list):
            list_of_tokens = []
            for sentence in example["text"]:
                list_of_tokens.extend(self.split(sentence))

            example["text"] = list_of_tokens
            return example
        example["text"] = self.split(example["text"])
        return example
