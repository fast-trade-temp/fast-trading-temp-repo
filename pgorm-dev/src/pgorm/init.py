from dependency_injector.wiring import Provide, inject
from src.pgorm.di.containers import Container
from src.pgorm.repositories.repository import QuoteRepositoryImpl
from datetime import datetime


@inject
def main(quote_repo: QuoteRepositoryImpl = Provide[Container.quote_repository]):
    quote_repo.drop()
    quote_repo.create()
    quote_repo.insert_csv(
        "C:\\Users\\Steven\\Desktop\\FastTrading\\fast-data-system\\data\\AA.csv"
    )

    quote_repo.insert("B", datetime.now(), 14.0, 13.0, 12.0, 10.0, 5)


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
