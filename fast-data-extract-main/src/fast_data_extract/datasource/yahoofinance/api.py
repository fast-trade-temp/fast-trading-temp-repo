from typing import Literal

_BASE_URL = "https://query1.finance.yahoo.com/"

Interval = Literal[
    "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"
]
Range = Literal["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
IncludePrePost = Literal["true", "false"]


def _urlgen(path: str, **kwargs) -> str:
    return f"{_BASE_URL}{path}?{'&'.join(f'{k}={v}' for k, v in kwargs.items())}"


class YahooFinanceAPI:
    @staticmethod
    def chart(
        symbol: str, interval: Interval, range: Range, include_pre_post: IncludePrePost
    ) -> str:
        return _urlgen(
            f"v8/finance/chart/{symbol}",
            symbol=symbol,
            interval=interval,
            range=range,
            includePrePost=include_pre_post,
        )


"https://query1.finance.yahoo.com/v8/finance/chart/TQQQ?symbol=TQQQ&period1=1660662000&period2=1661317908&useYfid=true&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=hUeRgl2wtfD&corsDomain=finance.yahoo.com"
"v8/finance/chart/TQQQ?symbol=TQQQ&period1=1660662000&period2=1661317908&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn"

"https://query1.finance.yahoo.com/v7/finance/download/TQQQ?period1=1629781947&period2=1661317947&interval=1d&events=split&includeAdjustedClose=true"
"https://query2.finance.yahoo.com/v1/finance/search?q=tqqq&lang=en-US&region=US&quotesCount=6&newsCount=2&listsCount=2&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&enableEnhancedTrivialQuery=true&enableResearchReports=true&enableCulturalAssets=true&researchReportsCount=2"
