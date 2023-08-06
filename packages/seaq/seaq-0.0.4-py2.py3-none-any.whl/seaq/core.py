import pandas as pd
import sqlite3
import pkg_resources
import re

PANDA_TYPES = {
    'float64': 'numeric',
    'int64': 'integer',
    'object': 'text',
    'datetime64[ns]': 'text',
    'datetime64': 'text'
}


def cast_to_db(x):
    return PANDA_TYPES.get(str(x), None)

#
# def infer_type(x, target='db'):
#     if target == 'db':


def infer_type_db(x):
    if x is None:
        return None
    if type(x) in (str, float, int, None):
        return x
    if hasattr(x, '_repr_base'):
        return x._repr_base


re_datetime = re.compile(r"\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2}(\.\d+)?)?")


def cast_series(series: pd.Series):
    if series.dtype == 'object':
        series.dropna(inplace=True)
        if all(re_datetime.match(x) for x in series):
            return series.astype('datetime64[ns]')
        else:
            return series
    else:
        return series


class SeaQuill:
    def __init__(self, path):
        self.db_path = path
        self.conn = sqlite3.connect(self.db_path)
        self.curr = self.conn.cursor()
        self.curr.execute(open(pkg_resources.resource_filename(__name__, 'sql/init.sql')).read())

    def __del__(self):
        self.conn.close()

    def to_db(self, obj: pd.DataFrame, table_name):
        # if object is not a pandas data frame, try to coerce it to one
        obj = obj if type(obj) is pd.DataFrame else pd.DataFrame(obj)

        self.drop_table(table_name, commit=False)
        data_types = [cast_to_db(dtype) for dtype in obj.dtypes]
        column_names = list(obj)
        self.create_table(table_name, column_names, data_types)
        self.insert(obj, table_name)
        self.commit()

    def get_query(self, query: str, params=()):
        self.curr.execute(query, params)
        rows = self.curr.fetchall()
        column_names = [x[0] for x in self.curr.description]
        data = pd.DataFrame(dict(zip(column_names, zip(*rows))))
        for column_name in column_names:
            data[column_name] = cast_series(data[column_name])
        return data

    def commit(self):
        self.conn.commit()

    def table_columns(self, table_name):
        self.curr.execute("SELECT * FROM {table_name} LIMIT 1".format(table_name=table_name))
        self.curr.fetchall()
        return [x[0] for x in self.curr.description]

    def insert(self, obj: pd.DataFrame, table_name: str):
        column_names = list(obj)
        sql = "INSERT INTO {table_name} ({columns}) VALUES ({qmarks})".format(
            table_name=table_name,
            columns=','.join(column_names),
            qmarks=','.join(':' + c for c in column_names)
        )
        self.curr.executemany(sql, (dict(zip(row._index, tuple(map(infer_type_db, row)))) for _, row in obj.iterrows()))

    def drop_table(self, table_name, commit=False):
        self.curr.execute("DROP TABLE IF EXISTS {table_name}".format(table_name=table_name))
        if commit:
            self.commit()

    def create_table(self, table_name, column_names, data_types, commit=False):
        sql_columns = ",".join([n + " " + t for n, t in zip(column_names, data_types)])
        sql = "CREATE TABLE IF NOT EXISTS {table_name} ({sql_columns})".\
            format(table_name=table_name, sql_columns=sql_columns)
        self.curr.execute(sql)
        if commit:
            self.commit()

    def from_db(self, table_name, limit: int = None):
        sql = "SELECT * FROM {table_name}".format(table_name=table_name)
        sql += " LIMIT {limit}".format(limit=limit) if type(limit) is int else ""
        data = self.get_query(sql)

        return data
