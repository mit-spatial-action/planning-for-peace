from pyalex import config, Works
from itertools import chain
import pandas as pd
import spacy
import re

def aii_to_text(index: dict) -> str:
    all_pos = [pos for positions in index.values() for pos in positions]

    if not all_pos:
        return ""

    abstract = [None] * (max(all_pos) + 1)

    for word, positions in index.items():
        for pos in positions:
            abstract[pos] = word

    return " ".join(word if word is not None else "" for word in abstract)


def nested_get(d, keys, default=None):
    """Safely get a nested value from a dictionary."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return default
    return d if d is not None else default


def concat_list(l: list, field: str = "display_name") -> str:
    if len(l) > 0:
        return ",".join([x[field] for x in l])
    return None


def parse_record(record: dict) -> dict:
    return {
        "oa_id": record.get("id"),
        "doi": record.get("doi"),
        "title": record.get("display_name"),
        "authors": concat_list(record.get("authorships", []), field="raw_author_name"),
        "publication": nested_get(record, ["primary_location", "source", "display_name"]),
        "year": record.get("publication_year"),
        "language": record.get("language"),
        "item_type": record.get("type"),
        "fwci": record.get("fwci"),
        "cited_by": record.get("cited_by_count"),
        "keywords": concat_list(record.get("keywords", [])),
        "topics": concat_list(record.get("topics", [])),
        "concepts": concat_list(record.get("concepts", [])),
        "abstract": (
            aii_to_text(record.get("abstract_inverted_index"))
            if record.get("abstract_inverted_index") is not None
            else None
        ),
    }


def get_openalex(query: str, email: str, n_max: int = None) -> pd.DataFrame:
    config.email = email
    config.max_retries = 2
    config.retry_backoff_factor = 0.1
    config.retry_http_codes = [429, 500, 503]

    q = Works().search_filter(title_and_abstract=query)
    results = [r for r in chain(*q.paginate(per_page=200, n_max=n_max))]
    return pd.DataFrame([parse_record(r) for r in results])


def clean_text(text, stopwords=None):
    if stopwords is None:
        stopwords = ["the", "a", "an", "and", "or", "but", "of", "to", "in"]
    
    text = text.strip()
    
    text = re.sub(r"(^|'s\b|'$)", "", text, flags=re.IGNORECASE).strip()
    
    text = re.sub(r"^[^\w]+|[^\w]+$", "", text)
    
    words = text.split()
    
    while words and words[0].lower() in stopwords:
        words.pop(0)
        
    while words and words[-1].lower() in stopwords:
        words.pop()

    return " ".join(words).upper()


def named_entities(df: pd.DataFrame, col: str, types: list = ["GPE"], model: str = "en_core_web_sm") -> pd.DataFrame:
    """Detect named entities in column"""
    nlp = spacy.load(model)
    results = [
        list(obj.text for obj in tup if obj.label_ in types)
        for tup in [
            i.ents for i in list(nlp.pipe(df[col], n_process=7))
        ]
    ]
    df["_".join([col, 'ents'])] = [None if len(tup) == 0 else tup for tup in results]
    
    df["_".join([col, 'ents'])] = df["_".join([col, 'ents'])].apply(
        lambda lst: [clean_text(s) for s in lst] if isinstance(lst, list) else []
    )
    return df

test = get_openalex("reparations", "ehuntley@mit.edu", n_max = 10000)
test2 = named_entities(test.dropna(subset=['title']), "title")

t3 = (
    test2.explode("title_ents")
        .groupby(["year", "title_ents"])     # group by year and term
        .size()                         # count occurrences
        .unstack(fill_value=0) 
        )

t3.plot()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "query",
        help="query passed to title_and_abstract.search in the OpenAlex API",
        type=str,
    )
    parser.add_argument(
        "-e", "--email", help="email to provide to OpenAlex API", type=str
    )
    args = parser.parse_args()

    get_openalex(query=args.query, email=args.email)
