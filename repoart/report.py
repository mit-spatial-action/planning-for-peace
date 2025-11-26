# -*- coding: utf-8 -*-

from pandas import DataFrame

from .config import ReportConfig


class OpenAlexReport:
    def __init__(self, config: ReportConfig):
        from .loaders import config_openalex
        self.config = config
        config_openalex(email=self.config.email)

    def get_works(self):
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

    def normalize_works(self):
        from .ner import normalize_columns, strip_spaces, to_lower, remove_extra_spaces, to_unicode
        self.works = normalize_columns(
            self.works,
            columns=self.config.cols,
            funcs=[strip_spaces, to_lower, remove_extra_spaces, to_unicode]
        )
        return self

    def recognize_entities(self):
        from .ner import recognize_entities
        self.works = recognize_entities(
            self.works,
            col="title",
            types=self.config.types,
            model=self.config.model
        )
        return self

    def missing_by(self, missing_field: str = "abstract", group_field: str = "year"):
        return (
            self.works
                .assign(miss=self.works[missing_field].isna())
                .groupby(group_field)
                .agg(total=('miss', 'size'),
                     missing=('miss', 'sum'))
                .assign(pct_missing=lambda d: 100 * d['missing'] / d['total'])
                .reset_index()
        )

# plot = (
#     ggplot(missing_by_year, aes('year', 'pct_missing')) +
#     geom_line()
# )

# t3 = (
#     test2.explode("title_ents")
#     .groupby(["year", "title_ents"])     # group by year and term
#     .size()                         # count occurrences
#     .unstack(fill_value=0)
# )

# test2['period'] = (test2['year'] // 10 ) * 10

# t3 = test2.explode("title_ents").groupby(['period', 'title_ents']).size().unstack(fill_value=0)

# t3.plot()


# t3 = (
#     test2.explode("title_ents")
#     .groupby(["title_ents"])     # group by year and term
#     .size()
# )
