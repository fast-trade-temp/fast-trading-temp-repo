from io import StringIO
from pathlib import Path

import fast_data_common.readers as readers
import pandas as pd


class StringReader(readers.Reader):
    @staticmethod
    def read(string: str) -> pd.DataFrame:
        """Alphavatange string reader

        The input csv should have the following columns: timestamp, open, high, low,
        close, volume.

        Args:
            buf (str): string to read

        Returns:
            pd.DataFrame: pandas dataframe
        """

        dataframe = pd.read_csv(StringIO(string), dtype=str)
        dataframe = dataframe.set_index(pd.to_datetime(dataframe["timestamp"]))
        dataframe = dataframe.drop(columns=["timestamp"])

        return dataframe


class CSVReader(readers.Reader):
    @staticmethod
    def read(path: Path) -> pd.DataFrame:
        """Alphavatange csv reader

        The input csv should have the following columns: timestamp, open, high, low,
        close, volume.

        Args:
            path (Path): path to read

        Returns:
            pd.DataFrame: pandas dataframe
        """

        dataframe = pd.read_csv(path, dtype=str)
        dataframe = dataframe.set_index(pd.to_datetime(dataframe["timestamp"]))
        dataframe = dataframe.drop(columns=["timestamp"])

        return dataframe
