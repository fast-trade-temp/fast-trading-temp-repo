# fast-data-extract

## Usage

```py
from pathlib import Path

from fast_data_common.types import DatasourceType

from fast_data_extract.fetcher.factory import DataFetcherFactory

data_fetch = DataFetcherFactory.get_fetcher_by_type(DatasourceType.ALPHAVANTAGE)
data_fetch.fetch(output_dir=Path("data/"), num_workers=16)
```

## Tests

```sh
python -m unittest discover
```
