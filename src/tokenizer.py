from tokenizers import BertWordPieceTokenizer, ByteLevelBPETokenizer, CharBPETokenizer


def build_tokenizer(args):
    tokenizer = None
    if args.tokenizer_type == "bbpe":
        tokenizer = ByteLevelBPETokenizer(unicode_normalizer="nfkc")
    elif args.tokenizer_type == "cbpe":
        tokenizer = CharBPETokenizer(
            unk_token="<unk>",
            unicode_normalizer="nfkc",
            bert_normalizer=False,
            split_on_whitespace_only=True,
        )
    elif args.tokenizer_type == "wp":
        tokenizer = BertWordPieceTokenizer(
            clean_text=False,
            handle_chinese_chars=True,
            strip_accents=False,
            lowercase=False,
        )
    return tokenizer
