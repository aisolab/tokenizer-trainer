import argparse
from pathlib import Path
from timeit import default_timer as timer

from datasets import load_dataset
from numpy.random import choice

from src.preprocessing import MorphemeSplitter, SentenceSplitter, SpaceSplitter
from src.tokenizer import build_tokenizer
from src.utils import convert_to_token_generator, extract_filepath_from_dir, get_logger


def get_args():
    parser = argparse.ArgumentParser()

    group = parser.add_argument_group(title="corpus")
    group.add_argument("--lang", type=str, default="ko")
    group.add_argument("--corpora-version", type=str, default="v00")

    group = parser.add_argument_group(title="preprocessing")
    group.add_argument("--sampling-ratio", type=float, default=0.01)
    group.add_argument("--split-to-sentences", action="store_true")
    group.add_argument("--split-to-morphemes", action="store_true")

    group = parser.add_argument_group(title="training")
    group.add_argument(
        "--tokenizer-type", type=str, choices=["bbpe", "cbpe", "wp"], default="bbpe"
    )
    group.add_argument("--vocab-size", default=30720),
    group.add_argument("--min-frequency", default=2),
    group.add_argument("--special-tokens", nargs="+", default=[])
    group.add_argument("--num-workers", type=int, default=8)
    group.add_argument("--seed", type=float, default=42)

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    root_dir = Path.cwd()
    corpora_dir = root_dir / "corpora"
    corpora_version_dir = corpora_dir / args.corpora_version
    list_of_filepath = extract_filepath_from_dir(corpora_version_dir)

    source_corpus = load_dataset(
        path="/home/user/workspace/src/loading/text.py",
        data_files=list_of_filepath,
        split="train",
    )

    logger = get_logger("tokenizer-trainer")

    logger.info(f"preprocessing start!")
    preprocessing_start_time = timer()

    preprocessed_corpus = source_corpus

    if args.sampling_ratio:
        total_size = len(preprocessed_corpus)
        sample_size = int(total_size * args.sampling_ratio)

        preprocessed_corpus = preprocessed_corpus.select(
            indices=choice(range(total_size), sample_size)
        )

    if args.split_to_sentences:
        sentence_splitter = SentenceSplitter(lang=args.lang)
        preprocessed_corpus = preprocessed_corpus.map(
            sentence_splitter.process, num_proc=args.num_workers
        )

    token_splitter = (
        MorphemeSplitter(lang=args.lang) if args.split_to_morphemes else SpaceSplitter()
    )

    preprocessed_corpus = preprocessed_corpus.map(
        token_splitter.process, num_proc=args.num_workers
    )

    preprocessing_end_time = timer()
    logger.info(
        f"preprocessing done!\nelapsed time {preprocessing_end_time - preprocessing_start_time:.4}s"
    )

    token_generator = convert_to_token_generator(preprocessed_corpus)
    tokenizer = build_tokenizer(args)

    logger.info(f"training start!")
    training_start_time = timer()

    tokenizer.train_from_iterator(
        iterator=token_generator,
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        special_tokens=args.special_tokens,
    )

    save_dir = root_dir / "vocab" / args.corpora_version
    if not save_dir.exists():
        save_dir.mkdir(parents=True)
    tokenizer.save_model(str(save_dir))

    training_end_time = timer()
    logger.info(f"training done!\nelapsed time {training_end_time - training_start_time:.4}s")


if __name__ == "__main__":
    main()
