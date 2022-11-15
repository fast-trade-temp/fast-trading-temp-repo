import re
import unittest

from fast_data_extract.proxy.hidemyname import Hidemyname
from fast_data_extract.proxy.spysone import SPYSONE


class TestGetProxies(unittest.TestCase):
    def test_get_spysone_proxies(self):

        proxy_provider = SPYSONE()
        proxy_pattern = re.compile(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}:\d{2,5}")
        proxy_count = 0

        for proxy in proxy_provider.iter_once():
            self.assertIsNotNone(re.match(proxy_pattern, str(proxy)))
            proxy_count += 1

        self.assertGreater(proxy_count, 0)

    def test_get_hidemyname_proxies(self):

        proxy_provider = Hidemyname()
        proxy_pattern = re.compile(r"\d{1,4}.\d{1,4}.\d{1,4}.\d{1,4}:\d{2,5}")
        proxy_count = 0

        for proxy in proxy_provider.iter_once():
            self.assertIsNotNone(re.match(proxy_pattern, str(proxy)))
            proxy_count += 1

        self.assertGreater(proxy_count, 0)


if __name__ == "__main__":
    unittest.main()
