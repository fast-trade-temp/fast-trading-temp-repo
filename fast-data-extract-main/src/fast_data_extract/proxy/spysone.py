from typing import List

from bs4 import BeautifulSoup
from fast_data_extract.proxy import Proxy, ProxyProvider
from js2py import EvalJs
from requests import Session


class SPYSONE(ProxyProvider):
    """
    Get proxies from https://spys.one/proxys/US/
    """

    def _get_host(self, soup: BeautifulSoup) -> str:
        # get all tds
        tds = soup.find_all("td")

        # only interested in td 1
        td = tds[0]

        return td.text

    def _get_port(self, soup: BeautifulSoup, ctx: EvalJs) -> str:
        # get all scripts
        scripts = soup.find_all("script")

        # only interested in script 1
        script = scripts[0]

        return "".join([str(ctx.eval(expr)) for expr in script.text[44:-1].split("+")])

    def _get_xf0(self, soup: BeautifulSoup) -> str:
        return soup.find("input", {"name": "xf0"}).get("value")

    def _get_ctx(self, soup: BeautifulSoup) -> EvalJs:
        # get scripts
        scripts = soup.find_all("script")

        # only interested in script 5
        script = scripts[4]

        ctx = EvalJs()
        ctx.execute(script.text)

        return ctx

    def get_proxies(self) -> List[Proxy]:
        proxies = []

        with Session() as session:
            session.headers.update({"User-Agent": "Mozilla/5.0"})

            # get page to obtain xf0
            res = session.get("https://spys.one/proxys/US/")
            soup = BeautifulSoup(res.text, "html.parser")

            # use xf0 to get page with proxies
            res = session.post(
                "https://spys.one/proxys/US/",
                {
                    "xpp": "5",
                    "xf1": "0",
                    "xf0": self._get_xf0(soup),
                    "xf2": "0",
                    "xf4": "0",
                    "xf5": "1",
                },
            )
            soup = BeautifulSoup(res.text, "html.parser")
            ctx = self._get_ctx(soup)

            # get tables
            tables = soup.find_all("table")

            # only interested in table 3
            table = tables[2]

            # get all table rows
            table_rows = table.find_all("tr")

            # only interested in rows starting from row 4 and ending with row -1
            table_rows = table_rows[3:-1]

            for table_row in table_rows[::2]:
                host = self._get_host(table_row)
                port = self._get_port(table_row, ctx)
                proxies.append(Proxy(host, port))

        return proxies
