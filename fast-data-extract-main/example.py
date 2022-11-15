from pathlib import Path

from fast_data_common.types import DatasourceType

from fast_data_extract.fetcher.factory import DataFetcherFactory

data_fetch = DataFetcherFactory.get_fetcher_by_type(DatasourceType.ALPHAVANTAGE)
data_fetch.fetch(Path("data/"), 16)
