import psycopg2
from abc import ABC, abstractmethod


class SQLDatabase(ABC):
    def __init__(self, user, password, host, port, db_name):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.connection = self.connect()

    def __enter__(self):
        self.active_cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.active_cursor.close()
        self.active_cursor = None

    def commit(self):
        self.connection.commit()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_and_fetch(self, sql):
        pass

    @abstractmethod
    def execute_and_fetch_one(self, sql):
        pass

    @abstractmethod
    def execute(self, sql):
        pass

    @abstractmethod
    def close(self):
        pass


class PostgresDatabaseImpl(SQLDatabase):
    def __init__(self, user: str, password: str, host: str, port: str, db_name: str):
        super().__init__(user, password, host, port, db_name)

    def connect(self):
        return psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name,
        )

    def execute_and_fetch(self, sql):
        self.active_cursor.execute(str(sql))
        self.connection.commit()
        data = self.active_cursor.fetchall()
        return data

    def execute_and_fetch_one(self, sql):
        self.active_cursor.execute(str(sql))
        self.connection.commit()
        data = self.active_cursor.fetchone()
        self.active_cursor.fetchall()
        return data

    def execute(self, sql):
        self.active_cursor.execute(str(sql))
        self.connection.commit()
        return True

    def close(self):
        self.connection.close()
        self.connection = None
