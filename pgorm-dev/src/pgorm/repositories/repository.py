from abc import abstractmethod
from datetime import datetime

from dependency_injector.wiring import inject
from src.pgorm.database.database import SQLDatabase
from src.pgorm.tables.table import Quotes, Symbols, Timestamps, QuotesPlaceholder


class Repository:
    @abstractmethod
    def create(self):
        raise NotImplementedError()

    @abstractmethod
    def drop(self):
        raise NotImplementedError()


class QuoteRepository(Repository):

    database: SQLDatabase

    @abstractmethod
    def get(self, symbol, start_date, end_date):
        pass

    @abstractmethod
    def insert(
        self,
        symbol: str,
        timestamp: datetime,
        open: float,
        high: float,
        close: float,
        low: float,
        volume: int,
    ):
        pass


class QuoteRepositoryImpl(QuoteRepository):
    @inject
    def __init__(
        self,
        database,
        quotes_table: Quotes,
        symbols_table: Symbols,
        timestamps_table: Timestamps,
    ):
        self.database = database
        self.quotes_table = quotes_table
        self.symbols_table = symbols_table
        self.timestamps_table = timestamps_table

    def create(self):
        with self.database as dbconn:
            dbconn.execute(self.symbols_table.create())
            dbconn.execute(self.timestamps_table.create())
            dbconn.execute(self.quotes_table.create())

    def drop(self):
        with self.database as dbconn:
            dbconn.execute(self.quotes_table.delete())
            dbconn.execute(self.timestamps_table.delete())
            dbconn.execute(self.symbols_table.delete())

    def insert(
        self,
        symbol: str,
        timestamp: datetime,
        open: float,
        high: float,
        close: float,
        low: float,
        volume: int,
    ):
        with self.database as dbconn:
            symbol_id = dbconn.execute_and_fetch_one(
                self.symbols_table.insert_values(symbol=symbol)
                .conflict_do_nothing(self.symbols_table.symbol)
                .returning(self.symbols_table.id)
            )

            if not symbol_id:
                symbol_id = dbconn.execute_and_fetch_one(
                    self.symbols_table.select(self.symbols_table.id).where(
                        self.symbols_table.symbol == f"'{symbol}'"
                    )
                )

            timestamp_id = dbconn.execute_and_fetch_one(
                self.timestamps_table.insert_values(timestamp=timestamp)
                .conflict_do_nothing(self.timestamps_table.timestamp)
                .returning(self.timestamps_table.id)
            )

            if not timestamp_id:
                timestamp_id = dbconn.execute_and_fetch_one(
                    self.timestamps_table.select(self.timestamps_table.id).where(
                        self.timestamps_table.timestamp
                        == f"'{timestamp.strftime('%Y-%m-%d %H:%M:%S')}'"
                    )
                )

            dbconn.execute(
                self.quotes_table.insert_values(
                    timestamp_id=timestamp_id[0],
                    symbol_id=symbol_id[0],
                    open=open,
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    is_interpolated=False,
                )
            )

    def get(self, symbol, start_date, end_date):
        with self.database as dbconn:
            data = dbconn.execute_and_fetch(
                self.quotes_table.select()
                .inner_join(
                    self.quotes_table.symbol_id,
                    self.symbols_table.select().where(
                        self.symbols_table.symbol == f"'{symbol}'"
                    ),
                    "fsymbols",
                    self.symbols_table.id,
                )
                .inner_join(
                    self.quotes_table.timestamp_id,
                    self.timestamps_table.select().where(
                        self.timestamps_table.timestamp.between(
                            f"'{start_date.strftime('%Y-%m-%d %H:%M:%S')}'",
                            f"'{end_date.strftime('%Y-%m-%d %H:%M:%S')}'",
                        )
                    ),
                    "ftimestamps",
                    self.timestamps_table.id,
                )
            )

            return data

    def insert_csv(self, csv_path):
        with self.database as dbconn:
            temp_table = QuotesPlaceholder()
            dbconn.execute(temp_table.create())

            dbconn.execute(temp_table.copy_from_csv(csv_path))

            timestamp_select = temp_table.select_distinct(temp_table.timestamp)
            symbol_select = temp_table.select_distinct(temp_table.symbol)

            dbconn.execute(
                self.timestamps_table.insert_select(
                    timestamp_select, self.timestamps_table.timestamp
                ).conflict_do_nothing(self.timestamps_table.timestamp)
            )

            dbconn.execute(
                self.symbols_table.insert_select(
                    symbol_select, self.symbols_table.symbol
                ).conflict_do_nothing(self.symbols_table.symbol)
            )

            dbconn.commit()

            dbconn.execute(
                self.quotes_table.insert_select(
                    temp_table.select(
                        temp_table.open,
                        temp_table.high,
                        temp_table.low,
                        temp_table.close,
                        temp_table.volume,
                    )
                    .inner_join_table(
                        temp_table.timestamp,
                        self.timestamps_table,
                        self.timestamps_table.timestamp,
                        self.timestamps_table.id,
                    )
                    .inner_join_table(
                        temp_table.symbol,
                        self.symbols_table,
                        self.symbols_table.symbol,
                        self.symbols_table.id,
                    ),
                    self.quotes_table.open,
                    self.quotes_table.high,
                    self.quotes_table.low,
                    self.quotes_table.close,
                    self.quotes_table.volume,
                    self.quotes_table.timestamp_id,
                    self.quotes_table.symbol_id,
                ).conflict_do_nothing()
            )

            dbconn.execute(temp_table.delete())
