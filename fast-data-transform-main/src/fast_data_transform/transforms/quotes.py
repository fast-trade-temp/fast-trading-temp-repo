from datetime import datetime
from fast_data_transform.transforms import Transform

import pandas as pd


class QuotesTransform(Transform):
    @staticmethod
    def transform(dataframe: pd.DataFrame) -> pd.DataFrame:

        dataframe = QuotesTransform.reindex(dataframe)
        dataframe = QuotesTransform.trim(dataframe)
        dataframe = QuotesTransform.interpolate(dataframe)

        return dataframe

    @staticmethod
    def reindex(dataframe: pd.DataFrame) -> pd.DataFrame:
        """Reindex with 1 minute intervals

        Args:
            dataframe (pd.DataFrame): pandas dataframe

        Returns:
            pd.DataFrame: reindexed pandas dataframe
        """

        dt = min(dataframe.index)

        dataframe = dataframe.reindex(
            pd.date_range(
                dt.replace(hour=0, minute=0, second=0),
                dt.replace(hour=23, minute=59, second=0),
                freq="T",
            )
        )

        return dataframe

    @staticmethod
    def trim(dataframe: pd.DataFrame) -> pd.DataFrame:
        """Trim pre/after market hour data

        Market hours starts at 9:30 and ends at 16:00 EST.

        Args:
            dataframe (pd.DataFrame): pandas dataframe

        Returns:
            pd.DataFrame: trimmed pandas dataframe
        """

        dataframe = dataframe.between_time("9:30", "16:00")

        return dataframe

    @staticmethod
    def interpolate(dataframe: pd.DataFrame) -> pd.DataFrame:
        """Interpolate missing market data

        - fill missing volumes with 0 (no activity)
        - forward fill missing opens, highs, lows, and closes with close
        - backward fill missing opens, highs, lows, and closes with open

        Args:
            dataframe (pd.DataFrame): pandas dataframe

        Returns:
            pd.DataFrame: interpolated pandas dataframe
        """

        dataframe["volume"] = dataframe["volume"].fillna("0")
        dataframe[["open", "high", "low", "close"]] = dataframe[
            ["open", "high", "low", "close"]
        ].fillna(dataframe["close"].ffill())
        dataframe[["open", "high", "low", "close"]] = dataframe[
            ["open", "high", "low", "close"]
        ].fillna(dataframe["open"].bfill())

        return dataframe
