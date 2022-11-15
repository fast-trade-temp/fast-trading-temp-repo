from pathlib import Path
from typing import Protocol

import pandas as pd


class Writer(Protocol):
    @staticmethod
    def write(dataframe: pd.DataFrame, path: Path):
        """Writer interface for writing dataframe to path

        The writer implementation must save the dataframe into a csv with the following
        columns: timestamp, open, high, low, close, volume.

        Example:
            timestamp,open,high,low,close,volume
            2022-10-10 20:00:00,19.0100,19.0200,19.0000,19.0100,31988
            2022-10-10 19:59:00,19.0000,19.0200,18.9900,19.0100,31758
            2022-10-10 19:58:00,18.9900,19.0100,18.9900,19.0000,39637
            2022-10-10 19:57:00,19.0100,19.0200,18.9900,19.0000,49254
            2022-10-10 19:56:00,19.0200,19.0200,19.0000,19.0100,27738

        Args:
            dataframe (pd.DataFrame): pandas dataframe
            path (Path): path to write

        Raises:
            NotImplementedError: not implemented
        """

        raise NotImplementedError()


class CSVWriter(Writer):
    @staticmethod
    def write(dataframe: pd.DataFrame, path: Path):
        """General csv writer

        The input dataframe should have datetime index and the following columns:
        timestamp, open, high, low, close, volume.

        Args:
            dataframe (pd.DataFrame): pandas dataframe
            path (Path): path to write
        """

        dataframe.to_csv(path, index_label="timestamp", mode="w+")
