# -*- coding: utf-8 -*-
import re
import string
import pandas as pd
import spacy
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


def recognize_entities(df: pd.DataFrame, col: str, types: list[str] = None, model: str = "en_core_web_lg") -> pd.DataFrame:
    """Detect named entities in column"""
    if types is None:
        types = ["GPE", "LOC"]
    disable = ["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]
    if model == "en_core_web_lg":
        import en_core_web_lg
        nlp = en_core_web_lg.load(disable=disable)
    elif model == "en_core_web_sm":
        import en_core_web_sm
        nlp = en_core_web_sm.load(disable=disable)
    else:
        sys.exit("Please specify either en_core_web_lg or en_core_web_sm")
    results = [
        list(obj.text for obj in tup if obj.label_ in types)
        for tup in [
            i.ents for i in list(nlp.pipe(df[col], n_process=7))
        ]
    ]
    df["_".join([col, 'ents'])] = [None if len(
        tup) == 0 else tup for tup in results]

    df["_".join([col, 'ents'])] = df["_".join([col, 'ents'])].apply(
        lambda lst: [normalize_text(s)
                     for s in lst] if isinstance(lst, list) else []
    )
    return df
