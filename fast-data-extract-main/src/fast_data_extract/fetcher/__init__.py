from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path

import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy


class Fetcher(ABC):

    date_format = "%Y-%m-%d"

    @property
    @abstractmethod
    def source(self) -> str:

        raise NotImplementedError()

    @abstractmethod
    def fetch(self, output_dir: Path, num_workers: int):

        raise NotImplementedError()

    @abstractmethod
    def aggregate_by_date(self, data: pd.DataFrame):

        raise NotImplementedError()

    @abstractmethod
    def save_to_fs(self, base_dir: Path, data: DataFrameGroupBy):

        raise NotImplementedError()
