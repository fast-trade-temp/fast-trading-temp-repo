from enum import Enum


class DatasourceType(str, Enum):
    ALPHAVANTAGE = "alphavantage"
    IEXCLOUD = "iexcloud"
    YAHOO_FINANCE = "yahoo_finance"
    POLYGON = "polygon"
    LOCAL = "local"


class ProxyType(str, Enum):
    HIDEMYNAME = "hidemyname"
    SPYSONE = "spysone"
