# -*- coding: utf-8 -*-

from .config import ReportConfig
from .loaders import get_works

class OpenAlexReport:
    def __init__(self, config: ReportConfig):
        self.config = config
        
    def run(self):
        df = get_works(
            query=self.config.query,
            start_year=self.config.start_year,
            end_year=self.config.end_year,
            work_types=self.config.work_types,
            domains=self.config.domains,
            n_max=self.config.n_max
        )
        return df

# df = get_works(
#     query=["reparation", "reparative", "reparatorial"],
#     start_year=1900,
#     end_year=2024,
#     work_types=["article", "book", "book-chapter"],
#     domains=["2"],
#     n_max=None
# )

# missing_by_year = (
#     df_init.assign(is_missing=df_init['abstract'].isna())
#       .groupby('year')
#       .agg(total=('is_missing', 'size'),
#            missing=('is_missing', 'sum'))
#       .assign(pct_missing=lambda d: 100 * d['missing'] / d['total'])
#       .reset_index()
# )

# plot = (
#     ggplot(missing_by_year, aes('year', 'pct_missing')) +
#     geom_line()
# )

# df_norm = normalize_columns(
#     df_init,
#     columns=["title", "abstract"],
#     funcs=[strip_spaces, to_lower, remove_extra_spaces, to_unicode]
# ).dropna(subset=['title'])

# t = df_norm.dropna(subset=["abstract"])

# test2 = named_entities(df_norm, "title")
# test3 = named_entities(t, "abstract")

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