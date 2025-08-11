from pyalex import config, Works
from itertools import chain
from csv import DictWriter
import json


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


def get_openalex(query: str, email: str) -> dict:
    config.email = email
    config.max_retries = 2
    config.retry_backoff_factor = 0.1
    config.retry_http_codes = [429, 500, 503]

    q = Works().search_filter(title_and_abstract=query)
    results = [r for r in chain(*q.paginate(per_page=200))]
    parsed = [parse_record(r) for r in results]
    with open("output.csv", "w", newline="", encoding="utf-8") as file:
        w = DictWriter(file, fieldnames=parsed[0].keys())
        w.writeheader()
        w.writerows(parsed)

    with open("output.json", "w", encoding="utf-8") as file:
        json.dump(results, file)
    return parsed


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
