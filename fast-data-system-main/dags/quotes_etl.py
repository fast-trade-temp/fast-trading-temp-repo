import datetime
import os
from pathlib import Path

import pendulum
from airflow.decorators import dag, task
from fast_fetching.datasource.alphavantage import pull_intraday


@dag(
    schedule_interval="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def quotes_etl():
    @task(do_xcom_push=True)
    def extract():
        # fetching data from data sources
        os.environ["no_proxy"] = "*"
        pull_intraday(Path(os.environ.get("QUOTES_ETL_DIR")))

    @task(do_xcom_push=True)
    def transform():
        # transforming fetched data
        pass

    @task(do_xcom_push=True)
    def load():
        # loading transformed data
        pass

    @task(do_xcom_push=False)
    def clean_up():
        # cleanup data
        pass

    extract() >> transform() >> load() >> clean_up()


dag = quotes_etl()
