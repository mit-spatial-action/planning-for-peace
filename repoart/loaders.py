# -*- coding: utf-8 -*-
from itertools import chain
from dataclasses import dataclass

import pandas as pd
from pyalex import config, Works

@dataclass
class Work:
    id: str
    doi: str | None
    title: str | None
    authors: str | None
    publication: str | None
    year: int
    language: str
    item_type: str
    fwci: float
    cited_by: int
    keywords: str | None
    topics: str | None
    concepts: str | None
    abstract: str | None
    

def config_openalex(email: str, max_retries: int = 2, retry_backoff_factor: float = 0.1, retry_http_codes: list | None = None):
    if retry_http_codes is None:
        retry_http_codes = [429, 500, 503]
    config.email = email
    config.max_retries = max_retries
    config.retry_backoff_factor = retry_backoff_factor
    config.retry_http_codes = retry_http_codes


def nested_get(d, keys, default=None):
    """Safely get a nested value from a dictionary."""
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return default
    return d if d is not None else default

def concat_list(l: list, field: str = "display_name") -> str:
    if not l:
        return None

    values = [x[field] for x in l if x.get(field) is not None]

    return ",".join(values) if values else None


def parse_record(record: dict) -> Work:
    return Work(
        id=record.get("id"),
        doi=record.get("doi"),
        title=record.get("display_name"),
        authors=concat_list(record.get("authorships", []),
                            field="raw_author_name"),
        publication=nested_get(
            record, ["primary_location", "source", "display_name"]),
        year=record.get("publication_year"),
        language=record.get("language"),
        item_type=record.get("type"),
        fwci=record.get("fwci"),
        cited_by=record.get("cited_by_count"),
        keywords=concat_list(record.get("keywords", [])),
        topics=concat_list(record.get("topics", [])),
        concepts=concat_list(record.get("concepts", [])),
        abstract=(
            aii_to_text(record.get("abstract_inverted_index"))
            if record.get("abstract_inverted_index") is not None
            else None
        )
    )

def aii_to_text(index: dict) -> str:
    all_pos = [pos for positions in index.values() for pos in positions]

    if not all_pos:
        return ""

    abstract = [None] * (max(all_pos) + 1)

    for word, positions in index.items():
        for pos in positions:
            abstract[pos] = word

    return " ".join(word if word is not None else "" for word in abstract)

def get_works(start_year: int, end_year: int, work_types: list[str], domains: list[str], languages: list[str], n_max: int = None, query: list[str] | None = None, group_col: str | None = None) -> pd.DataFrame:
    q = Works().filter(
        type='|'.join(work_types),
        primary_topic={"domain": {"id": '|'.join(domains)}},
        publication_year=f"{start_year}-{end_year}",
        language='|'.join(languages)
    )
    
    if query:
        q = q.search_filter(
            title_and_abstract='|'.join(query)
        )
        
    if group_col:
        q = q.group_by(group_col)
    
    results = list(chain(*q.paginate(per_page=200, n_max=n_max)))
    
    if group_col:
        results = []
        for r in results:
            results += [{group_col: int(r["key"]), "count": r["count"]}]
    else:
        group_col = "id"
        results = [parse_record(r) for r in results]
        
    return pd.DataFrame(results).set_index(group_col)

def get_works_prop(query: list[str], start_year: int, end_year: int, work_types: list[str], domains: list[str], languages: list[str], group_col: str | None = None):
    df = get_works(
        start_year=start_year,
        end_year=end_year,
        work_types=work_types,
        domains=domains,
        languages=languages,
        query=query,
        group_col=group_col
    )
    baseline = get_works(
        start_year=start_year,
        end_year=end_year,
        work_types=work_types,
        domains=domains,
        languages=languages,
        group_col=group_col
    )

    df = baseline.join(df, lsuffix="_tot").fillna(0)
    df["prop"] = df["count"] / df["count_tot"]
    return df