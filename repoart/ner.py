# -*- coding: utf-8 -*-
import re
import string
import pandas as pd
from unidecode import unidecode
import sys


def normalize_text(
    s: str | None,
    stopwords: list[str] | None = None
) -> str | None:
    """
    Remove stopwords, replace punctuation with spaces, collapse extra whitespace,
    and produce a trimmed, clean string. If input is None, returns None.
    """
    if s is None:
        return None

    if stopwords is None:
        stopwords = ["the", "a", "an", "of", "and", "to", "in"]

    # Convert to lowercase
    s = s.lower()

    # Replace punctuation with space
    # (punctuation = !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
    s = re.sub(f"[{re.escape(string.punctuation)}]", " ", s)

    # Split into tokens
    tokens = s.split()

    # Remove stopwords
    tokens = [t for t in tokens if t not in stopwords]

    # Join tokens back
    return " ".join(tokens)


def strip_spaces(s: str) -> str:
    return s.strip()


def to_lower(s: str) -> str:
    return s.lower()


def remove_extra_spaces(s: str) -> str:
    return " ".join(s.split())


def to_unicode(s: str) -> str:
    return unidecode(s)


def apply_funcs(x, funcs):
    if x in [None, "None", "nan"]:
        return None
    for f in funcs:
        x = f(x)
    return x


def normalize_columns(df: pd.DataFrame, columns, funcs):
    """
    Apply a sequence of string-normalization functions to multiple DataFrame columns.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe.
    columns : list[str]
        Column names to normalize.
    funcs : list[callable]
        List of functions that accept and return a string or None.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with normalized columns.
    """
    df = df.copy()

    for col in columns:
        df[col] = df[col].astype(str).map(lambda x: apply_funcs(x, funcs))

    return df.replace(r'^\s*$', None, regex=True)

def recognize_entities(df: pd.DataFrame, col: str, types: list[str] = None, n_process: int = 1, model: str = "en_core_web_lg") -> pd.DataFrame:
    """Detect named entities in column"""
    import spacy
    if types is None:
        types = ["GPE", "LOC"]
    if model not in ["en_core_web_lg", "en_core_web_sm"]:
        raise ValueError("Model must be either 'en_core_web_lg' or 'en_core_web_sm'.")
    nlp = spacy.load(model)
    
    # Extract the column as a list
    texts = df[col].tolist()

    # Identify valid (string) rows for nlp.pipe
    indexed = [
        (i, t) for i, t in enumerate(texts)
        if isinstance(t, str) and t.strip()
    ]

    if indexed:
        idx, valid_texts = zip(*indexed)
        processed_docs = list(
            nlp.pipe(
                valid_texts,
                disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"],
                n_process=n_process
            )
        )
    else:
        idx, processed_docs = [], []
    
    results = [[] for _ in texts]
    
    for i, doc in zip(idx, processed_docs):
        ents = [ent.text for ent in doc.ents if ent.label_ in types]
        results[i] = ents

    ent_col = f"{col}_ents"
    df[ent_col] = [
        None if len(lst) == 0 else [normalize_text(s) for s in lst]
        for lst in results
    ]

    return df
