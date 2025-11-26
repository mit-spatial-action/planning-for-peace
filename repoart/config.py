# -*- coding: utf-8 -*-

from dataclasses import dataclass
import tomllib


@dataclass
class BaseConfig:
    @classmethod
    def from_toml(cls, path):
        with open(path, "rb") as f:
            data = tomllib.load(f)
        return cls(**data)


@dataclass
class ReportConfig(BaseConfig):
    query: list[str]
    start_year: int
    end_year: int
    work_types: list[str]
    domains: list[str]
    languages: list[str]
    email: str
    cols: list[str] = ["title", "abstract"]
    types: list[str] = ["GPE", "LOC"]
    model: str = "en_core_web_lg"
    n_max: int | None = None
