from src.pgorm.constraint import ForeignKey, PrimaryKey, Unique
from src.pgorm.datatype import (
    CharacterVarying,
    Integer,
    Numeric,
    Serial,
    Timestamp,
    Boolean,
)

from src.pgorm.field import Field
from src.pgorm.table import Table


@PrimaryKey(("id",))
@Unique(("timestamp",))
class Timestamps(Table):
    id = Field("id", Serial(), not_null=True)
    timestamp = Field("timestamp", Timestamp(0), not_null=True)


@PrimaryKey(("id",))
@Unique(("symbol",))
class Symbols(Table):
    id = Field("id", Serial(), not_null=True)
    symbol = Field("symbol", CharacterVarying(10), not_null=True)


@PrimaryKey(("timestamp_id", "symbol_id"))
@ForeignKey(("timestamp_id",), "timestamps", ("id",))
@ForeignKey(("symbol_id",), "symbols", ("id",))
class Quotes(Table):
    timestamp_id = Field("timestamp_id", Integer(), not_null=True)
    symbol_id = Field("symbol_id", Integer(), not_null=True)
    open = Field("open", Numeric(10, 2), not_null=True)
    high = Field("high", Numeric(10, 2), not_null=True)
    low = Field("low", Numeric(10, 2), not_null=True)
    close = Field("close", Numeric(10, 2), not_null=True)
    volume = Field("volume", Integer(), not_null=True)
    is_interpolated = Field(
        "is_interpolated", Boolean(), not_null=True, default_val=False
    )


class QuotesPlaceholder(Table):
    timestamp = Field("timestamp", Timestamp(0), not_null=True)
    symbol = Field("symbol", CharacterVarying(10), not_null=True)
    open = Field("open", Numeric(10, 2), not_null=True)
    high = Field("high", Numeric(10, 2), not_null=True)
    low = Field("low", Numeric(10, 2), not_null=True)
    close = Field("close", Numeric(10, 2), not_null=True)
    volume = Field("volume", Integer(), not_null=True)
