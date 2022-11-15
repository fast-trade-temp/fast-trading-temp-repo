from dependency_injector import containers, providers
from src.pgorm.database.database import PostgresDatabaseImpl
from src.pgorm.repositories.repository import QuoteRepositoryImpl
from src.pgorm.tables.table import Timestamps, Symbols, Quotes


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["src//pgorm//config.yml"])
    database = providers.Singleton(
        PostgresDatabaseImpl,
        user=config.credentials.user,
        password=config.credentials.password,
        host=config.credentials.host,
        port=config.credentials.port,
        db_name=config.credentials.database,
    )

    timestamps_table = providers.Factory(
        Timestamps,
    )

    symbols_table = providers.Factory(
        Symbols,
    )

    quotes_table = providers.Factory(
        Quotes,
    )

    quote_repository = providers.Factory(
        QuoteRepositoryImpl,
        database=database,
        quotes_table=quotes_table,
        symbols_table=symbols_table,
        timestamps_table=timestamps_table,
    )
