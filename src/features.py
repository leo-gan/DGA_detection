from typing import List
from collections import Counter
import pandas as pd
from transformers import DistilBertTokenizer


def extract_tokens_features(s: str, max_length: int = 14, tokenizer=None) -> List[int]:
    """
    Transform a string into a sequence of tokens; then into the lengths of the tokens;
    then into the counters of lengths from 1 to 14.
    Tokens with lengths > 14 counted as 14 length. It is super rare when a token has a length > 14.
    """
    d = dict(
        Counter(
            [
                len(t.replace("##", ""))
                for t in tokenizer.convert_ids_to_tokens(tokenizer(s)["input_ids"])
                if t not in ["[CLS]", "[SEP]", "."]
            ]
        )
    )
    features = [d[i] if i in d else 0 for i in range(1, 19)]
    features_cut = features[: max_length - 1] + [sum(features[max_length:])]
    return features_cut


def prepare_old_features(df, tokenizer, out_dir=None, nrows=None):
    df = df[:nrows].copy(deep=True)
    df['features'] = df['domain'].apply(lambda d: extract_tokens_features(d, max_length=14, tokenizer=tokenizer))
    df['y'] = df['label'].apply(lambda d: 0 if d == 'bening' else 1)
    
    if out_dir:
        out_file = f"{out_dir}/data.csv"
        df.to_csv(out_file, index=False)
        print(f"Saved {df.shape[0]:,} {out_file}") 
    return df


def extract_bytes_features(s: str, pad_char: str = "=", max_len=20) -> List[int]:
    """
    It converts a string into the features.
    Features are the bytes decoded from the string.
    The feature array is taken from the middle of the string if the string is longer than max_len;
    the string is padded with a pad char if it is shorter than max_len.
    """
    if isinstance(s, bytes):
        s = s.decode()
    elif not isinstance(s, (str, bytes)):
        raise ValueError(s, "Only str or bytearray type can be processed.")

    s_len = len(s)
    if s_len < max_len:
        s = s + pad_char * (max_len - s_len)
    elif s_len > max_len:
        delta = (s_len - max_len) // 2
        s = s[delta : (max_len + delta)]

    return [ord(b) for b in s]


def prepare_bytes_features(df, out_dir=None, max_len=20, nrows=None):
    print(f"{df.shape=} max_len={max_len} nrows={nrows}")
    df = df[:nrows].copy(deep=True)
    print(f"Start with {df.shape[0]:,} samples")
    df = df.dropna()
    print(f"After dropna {df.shape[0]:,} samples")
    df['features'] = df['domain'].apply(lambda d: extract_bytes_features(d, max_len=max_len))
    df['y'] = df['label'].apply(lambda d: 0 if d == 'bening' else 1)
    
    if out_dir:
        out_file = f"{out_dir}/data.csv"
        df.to_csv(out_file, index=False)
        print(f"Saved {df.shape[0]:,} {out_file}") 
    return df


def extract_ensemble_features(s: str, pad_char: str = "=", max_len=20, max_token_num: int = 14, tokenizer=None) -> List[int]:
    """
    Extract both token and byte features and concatenate them.
    This corresponds to the ensemble model features.
    """
    return (extract_tokens_features(s, max_length=max_token_num, tokenizer=tokenizer)
           + extract_bytes_features(s, pad_char=pad_char, max_len=max_len))


def prepare_ensemble_features(df, out_dir=None, max_len=20, nrows=None, save=False):
    """
    Prepare ensemble features for a dataframe.
    """
    print(f"{df.shape=} {max_len=} {nrows=} ")
    df = df[:nrows].copy(deep=True)
    print(f"Start with {df.shape[0]:,} samples")
    df = df.dropna()
    print(f"After dropna {df.shape[0]:,} samples")
    
    # Load tokenizer
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    
    df['features'] = df['domain'].apply(lambda d: extract_ensemble_features(
        d, max_len=max_len,
        tokenizer=tokenizer
    ))
    df['y'] = df['label'].apply(lambda d: 0 if d == 'bening' else 1)
    
    if save and out_dir:
        import os
        os.makedirs(out_dir, exist_ok=True)
        out_file = f"{out_dir}/data.csv"
        df.to_csv(out_file, index=False)
        print(f"Saved {df.shape[0]:,} {out_file}") 
    print(f"Result  {df.shape[0]:,}")
    return df
