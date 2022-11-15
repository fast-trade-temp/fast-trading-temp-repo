from pathlib import Path
from typing import ClassVar

import pandas as pd
from fast_data_common.readers.alphavantage import CSVReader
from fast_data_common.writers import CSVWriter
from fast_data_extract.datasource.alphavantage import pull_intraday
from fast_data_extract.fetcher import Fetcher
from pandas import Series
from pandas.core.groupby.generic import DataFrameGroupBy


class AlphavantageFetcher(Fetcher):

    source: ClassVar[str] = "Alphavantage"

    def fetch(self, output_dir: Path, num_workers: int):

        for result in pull_intraday(num_workers):
            data = self.aggregate_by_date(result)
            self.save_to_fs(output_dir, data)

    def aggregate_by_date(self, data: pd.DataFrame):

        data = data.groupby(data.index.day)
        return data

    def save_to_fs(self, base_dir: Path, data: DataFrameGroupBy):

        for _, frame in data:
            symbol = frame["symbol"]
            timestamp = frame.index.strftime(self.date_format)

            assert self.is_not_unique(symbol)
            assert self.is_not_unique(timestamp)

            symbol = symbol.iloc[0]
            timestamp = timestamp[0]

            save_path = base_dir / self.source / timestamp
            save_path.mkdir(parents=True, exist_ok=True)

            existing_csv_path = (
                base_dir / self.source / timestamp / symbol
            ).with_suffix(".csv")

            if existing_csv_path.exists():
                existing_frame = CSVReader.read(existing_csv_path)
                existing_frame.update(frame)
                frame = existing_frame

            CSVWriter.write(frame, existing_csv_path)

    def is_not_unique(self, series: Series) -> bool:
        
        series = series.to_numpy()

        return (series[0] == series).all(0)
