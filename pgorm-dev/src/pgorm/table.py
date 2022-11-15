from src.pgorm.tables.insert import Insert
from src.pgorm.tables.select import Select
from src.pgorm.field import Field
import inspect


class Table:
    def __init__(self):
        self._fields = dict()
        self._constraints = []
        for k, v in inspect.getmembers(self):
            if isinstance(v, Field):
                self._fields[v.name] = v

    def __repr__(self) -> str:
        return self.__class__.__name__.lower()

    def create(self) -> str:
        props = [f"{prop}" for prop in list(self._fields.values()) + self._constraints]
        return f"CREATE TABLE IF NOT EXISTS {self} ({', '.join(props)});"

    def delete(self) -> str:
        return f"DROP TABLE IF EXISTS {self};"

    def select(self, *fields) -> Select:
        return Select(self, False, *fields)

    def select_distinct(self, *fields) -> Select:
        return Select(self, True, *fields)

    def insert_values(self, **kwargs) -> Insert:
        columns = []
        values = []
        for key, value in kwargs.items():
            field = self._fields[key]
            if type(value) is not field.data_type.python_type():
                raise TypeError
            columns.append(key)
            values.append(field.data_type.to_sql(value))
        return Insert(self, columns, values)

    def insert_select(self, select: Select, *fields) -> Insert:
        return Insert(self, columns=[field.name for field in fields], select=select)

    def copy_from_csv(self, csv_path):
        with open(csv_path, "r") as csv:
            headers = csv.readline().strip().split(",")
            return f"COPY {self.__repr__()} ({', '.join(headers)}) FROM '{csv_path}' DELIMITER ',' CSV HEADER"
