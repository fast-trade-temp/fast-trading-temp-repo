from typing import Protocol

import pandas as pd


class Transform(Protocol):
    @staticmethod
    def transform(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Transform data

        Raises:
            NotImplementedError: not implemented

        Returns:
            pd.DataFrame: pandas dataframe
        """

        raise NotImplementedError()
