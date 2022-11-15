from fast_data_common.types import DatasourceType
from fast_data_extract.fetcher import Fetcher
from fast_data_extract.fetcher.data import AlphavantageFetcher


class DataFetcherFactory:
    def get_fetcher_by_type(type: DatasourceType) -> Fetcher:
        if type == DatasourceType.ALPHAVANTAGE:
            return AlphavantageFetcher()
        else:
            raise NotImplementedError
