import argparse
from pathlib import Path

from tokenizers import ByteLevelBPETokenizer

from src.preprocessing import pretokenize_collator, string_sampler
from src.pretokenization import split_to_eojeol
from src.reader import read_corpora


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpora-version", type=str, default="test")
    parser.add_argument("--sampling-ratio", type=float, default=0.01)
    parser.add_argument("--seed", type=float, default=42)
    args = parser.parse_args([])
    return args


def main():
    # TODO: logger 추가
    args = get_args()

    root_dir = Path.cwd()
    corpora_dir = root_dir / "corpora"
    corpora_version_dir = corpora_dir / args.corpora_version
    corpora_gen = pretokenize_collator(
        string_sampler(read_corpora(corpora_version_dir)), split_to_eojeol
    )

    tokenizer = ByteLevelBPETokenizer(unicode_normalizer="nfkc")
    tokenizer.train_from_iterator(
        corpora_gen,
        vocab_size=100,
        min_frequency=2,
        show_progress=True,
    )
    # TODO: line을 token단위로 정리하기


if __name__ == "__main__":
    main()
