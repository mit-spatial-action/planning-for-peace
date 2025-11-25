# -*- coding: utf-8 -*-

from dataclasses import dataclass

@dataclass
class ReportConfig:
    data_path: str
    start_year: int
    end_year: int
    work_types: list[str]
    domains: list[str]
    n_max: int | None = None