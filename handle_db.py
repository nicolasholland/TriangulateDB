import pandas as pd
import sqlite3
import uuid

class DBHandle(object):

    def __init__(self) -> None:
        self.conn = sqlite3.connect('triangulate.db')

        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS uuid_mapping (
            uuid TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL
        )
        '''
        )

    @staticmethod
    def gen_uuid():
        """ Create a uuid """
        table_uuid = uuid.uuid4()
        table_name = "UUID_" + str(table_uuid).replace('-', '_')
        return table_name

    def insert_geocoord(self, table_name: str,
                        latitude: float, longitude: float):
        """
        Insert geo coords into uuid_mapping table
        """
        uuid_query = f'''
        INSERT INTO uuid_mapping (uuid, latitude, longitude)
        VALUES ("{table_name}", {latitude}, {longitude})
        '''
        self.conn.execute(uuid_query)

    def insert_ts(self, ts: pd.Series, table_name: str):
        """ Insert timeseries under table name of uuid """
        ts.to_sql(table_name, self.conn, if_exists='replace')

    def get_geotable(self):
        uuid_mapping_df = pd.read_sql_query('SELECT * FROM uuid_mapping', self.conn)
        return uuid_mapping_df

    def get_ts(self, geoid: str):
        query = f'SELECT * FROM {geoid}'
        time_series = pd.read_sql_query(query, self.conn)
        time_series = time_series.set_index("Datetime")
        return time_series

    def get_all_tables(self):
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = self.conn.execute(tables_query).fetchall()
        return tables

