# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
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
    cols: list[str] = field(default_factory=lambda: ["title", "abstract"])
    types: list[str] = field(default_factory=lambda: ["GPE", "LOC"])
    model: str = "en_core_web_lg"
    n_max: int | None = None
