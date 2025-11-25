# -*- coding: utf-8 -*-
from itertools import chain
import pandas as pd
from pyalex import config, Works

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

def aii_to_text(index: dict) -> str:
    all_pos = [pos for positions in index.values() for pos in positions]

    if not all_pos:
        return ""

    abstract = [None] * (max(all_pos) + 1)

    for word, positions in index.items():
        for pos in positions:
            abstract[pos] = word

    return " ".join(word if word is not None else "" for word in abstract)

def concat_list(l: list, field: str = "display_name") -> str:
    if not l:
        return None

    values = [x[field] for x in l if x.get(field) is not None]

    return ",".join(values) if values else None

def get_works(query: list[str], start_year: int, end_year: int, work_types: list[str], domains: list[str], n_max: int = None) -> pd.DataFrame:
    q = Works().filter(
        type='|'.join(work_types),
        publication_year=f"{start_year}-{end_year}",
        primary_topic={"domain": {"id": '|'.join(domains)}}
    ).search_filter(
        title_and_abstract='|'.join(query)
    )
    results = list(chain(*q.paginate(per_page=200, n_max=n_max)))
    results = [parse_record(r) for r in results]
    results = pd.DataFrame(results)
    return results.set_index("oa_id")

def get_works_count_by_year(start_year: int, end_year: int, work_types: list[str], domains: list[str], languages: list[str], query: list[str] | None = None):
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
        
    q = q.group_by("publication_year")
    results = list(chain(*q.paginate(per_page=200, n_max=None)))
    
    counts = []
    for r in results:
        counts += [{"year": int(r["key"]), "count": r["count"]}]
        
    df = pd.DataFrame(counts)
    return df.set_index("year")

def get_works_prop_by_year(query: list[str], start_year: int, end_year: int, work_types: list[str], domains: list[str], languages: list[str]):
    df = get_works_count_by_year(
        start_year=start_year,
        end_year=end_year,
        query=query,
        work_types=work_types,
        domains=domains,
        languages=languages
    )
    baseline = get_works_count_by_year(
        start_year=start_year,
        end_year=end_year,
        work_types=work_types,
        domains=domains,
        languages=languages
    )

    df = baseline.join(df, lsuffix="_tot").fillna(0)
    df["prop"] = df["count"] / df["count_tot"]
    return df