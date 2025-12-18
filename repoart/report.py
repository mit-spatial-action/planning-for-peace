# -*- coding: utf-8 -*-

from pandas import DataFrame

from plotnine import *
from .config import ReportConfig


class OpenAlexReport:
    def __init__(self, config: ReportConfig):
        from .loaders import config_openalex
        self.config = config
        config_openalex(email=self.config.email)

    def _get_works(self):
        from .loaders import get_works
        self.works = get_works(
            query=self.config.query,
            start_year=self.config.start_year,
            end_year=self.config.end_year,
            work_types=self.config.work_types,
            domains=self.config.domains,
            languages=self.config.languages,
            n_max=self.config.n_max
        )
        return self
    
    def _get_works_prop(self):
        from .loaders import get_works_prop
        self.works_prop = get_works_prop(
            query=self.config.query,
            start_year=self.config.start_year,
            end_year=self.config.end_year,
            work_types=self.config.work_types,
            domains=self.config.domains,
            languages=self.config.languages,
            group_col="publication_year"
        )
        return self
        
    def _plt_works_prop(self, window: int=3):
        self.works_prop_plot = (
            ggplot(self.works_prop, aes(x=self.works_prop.index, y="prop"))
            + geom_line()
            + labs(
                title=f"Proportional Frequency of Terms {', '.join(self.config.query)}",
                x="Year",
                y="Percent of Literature")
            + geom_smooth(
                method="mavg", 
                se=False,
                color="red",
                size=0.5,
                method_args={'window': window, 'center': True}
            )
        )
        return self

    def _normalize_works(self):
        from .ner import normalize_columns, strip_spaces, to_lower, remove_extra_spaces, to_unicode
        self.works = normalize_columns(
            self.works,
            columns=self.config.cols,
            funcs=[strip_spaces, to_lower, remove_extra_spaces, to_unicode]
        )
        return self

    def _recognize_entities(self):
        from .ner import recognize_entities
        self.works = recognize_entities(
            self.works,
            col="title",
            types=self.config.types,
            model=self.config.model
        )
        return self

    def _missing_by(self, missing_field: str = "abstract", group_field: str = "year"):
        return (
            self.works
                .assign(miss=self.works[missing_field].isna())
                .groupby(group_field)
                .agg(total=('miss', 'size'),
                     missing=('miss', 'sum'))
                .assign(pct_missing=lambda d: 100 * d['missing'] / d['total'])
                .reset_index()
        )
    
    def _get_ne(self):
        from loaders import get_ne_states, get_ne_map_units, get_ne_populated_places
        self.states = get_ne_states()
        self.map_units = get_ne_map_units()
        self.places = get_ne_populated_places()
        return self

    def _norm_ne(self):
        from .ner import normalize_columns, strip_spaces, to_lower, remove_extra_spaces, to_unicode
        self.states_norm = normalize_columns(
            self.states,
            columns=["name", "name_alt"],
            funcs=[strip_spaces, to_lower, remove_extra_spaces, to_unicode]
        )[["adm1_code", "name", "name_alt", "geometry"]]
    
    def run(self):
        self._get_works_prop()
        self._plot_works_prop()
        self._get_works()
        self._normalize_works()
        self._recognize_entities()
        
        return self.results