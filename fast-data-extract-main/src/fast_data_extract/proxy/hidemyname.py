from typing import List

from bs4 import BeautifulSoup
from fast_data_extract.proxy import Proxy, ProxyProvider
from requests import Session


class Hidemyname(ProxyProvider):
    """
    Get proxies from https://hidemy.name/en/proxy-list

    Note:
        As of 2022-08-25, Hidemyname proxies can be scraped with the following steps:
         1) Paginating using the "start" query parameter starting at 0. Each page has 64
            proxies hence to avoid duplicates, "start" must be incremented by 64.
         2) Scraping the first table of each page. Each page only contains 1 table.
    """

    def _get_host(self, soup: BeautifulSoup) -> str:
        return soup.find_all("td")[0].text

    def _get_port(self, soup: BeautifulSoup) -> str:
        return soup.find_all("td")[1].text

    def get_proxies(self) -> List[Proxy]:
        proxies = []

        with Session() as session:
            session.headers.update({"User-Agent": "Mozilla/5.0"})
            start = 0

            while True:
                res = session.get(
                    f"https://hidemy.name/en/proxy-list?country=US&type=hs&{start=}"
                )
                soup = BeautifulSoup(res.text, "html.parser")

                # get tables
                tables = soup.find_all("table")

                # only interested in table 1
                table = tables[0]

                # get all table rows
                table_rows = table.find_all("tr")

                # only interested in rows starting from row 2
                table_rows = table_rows[1:]

                if len(table_rows) == 0:
                    break

                for table_row in table_rows:
                    host = self._get_host(table_row)
                    port = self._get_port(table_row)
                    proxies.append(Proxy(host, port))

                start += 64

        return proxies
