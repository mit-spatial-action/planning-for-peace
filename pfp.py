#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 09:18:38 2025

@author: ehuntley
"""

from repoart.report import OpenAlexReport
from repoart.config import ReportConfig

oar = OpenAlexReport(ReportConfig.from_toml("pfp.toml"))

oar.get_works().normalize_works()

oar.recognize_entities()