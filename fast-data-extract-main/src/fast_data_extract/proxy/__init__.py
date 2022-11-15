from abc import abstractmethod
from dataclasses import dataclass
from itertools import cycle
from time import time
from typing import Iterator, List

import requests


@dataclass(frozen=True)
class Proxy:
    host: str
    port: str

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"

    def __repr__(self) -> str:
        return f"{self.host}:{self.port}"


class ProxyProvider:
    """
    Base Class ProxyProvider
    """

    def __init__(self):
        self.proxies = self.get_proxies()

    def measure(self, url: str):
        # TODO: Refactor
        for proxy in self.proxies:

            try:
                beg = time()
                requests.get(url, proxies={"http": proxy})
                end = time()
                print(proxy, f"took: {end - beg}s")

            except ConnectionError:
                print(proxy, "failed")

    def iter_once(self) -> Iterator[Proxy]:
        for proxy in self.proxies:
            yield proxy

    def iter_forever(self) -> Iterator[Proxy]:
        for proxy in cycle(self.proxies):
            yield proxy

    def __len__(self) -> int:
        return len(self.proxies)

    @abstractmethod
    def get_proxies(self) -> List[Proxy]:
        raise NotImplementedError()


class ProxyProviders:
    def __init__(self, *proxy_providers: ProxyProvider):
        pass
