# fast-data-transform

## Usage

```py
from pathlib import Path

from fast_data_common.readers.alphavantage import CSVReader
from fast_data_common.writers import CSVWriter

from fast_data_transform.transforms.quotes import QuotesTransform

dataframe = CSVReader.read("TQQQ.csv")
dataframe = QuotesTransform.transform(dataframe)
CSVWriter.write(dataframe, Path("TQQQ_transformed.csv"))
```
