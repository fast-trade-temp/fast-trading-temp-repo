from pathlib import Path
from typing import Protocol

import pandas as pd


class Reader(Protocol):
    @staticmethod
    def read(path: Path) -> pd.DataFrame:
        """Reader interface for reading dataframe from path

        The reader implementation must load the csv into a dataframe with a datetime
        index and the following columns: timestamp, open, high, low, close, volume.

        Example:
                                    open     high      low    close volume
            timestamp
            2022-10-10 20:00:00  19.0100  19.0200  19.0000  19.0100  31988
            2022-10-10 19:59:00  19.0000  19.0200  18.9900  19.0100  31758
            2022-10-10 19:58:00  18.9900  19.0100  18.9900  19.0000  39637
            2022-10-10 19:57:00  19.0100  19.0200  18.9900  19.0000  49254
            2022-10-10 19:56:00  19.0200  19.0200  19.0000  19.0100  27738

        Args:
            path (Path): path to read

        Raises:
            NotImplementedError: not implemented

        Returns:
            pd.DataFrame: pandas dataframe
        """

        raise NotImplementedError()
