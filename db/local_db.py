
from psycopg2 import pool
from configs import config
from utility import app_constants
import pandas
import pandas.io.sql as sql
from sqlalchemy import create_engine, URL
sql_db_pool = None 

class SqlDataPool:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, props:config.AppConfig):
        if not hasattr(self , '_initialized'):
            url=URL.create(
                        drivername=props.get(app_constants.APP_LOCAL_DB_DRIVER_NAME),
                        username=props.get(app_constants.APP_LOCAL_DB_USER_NAME),
                        password=props.get(app_constants.APP_LOCAL_DB_PSSWORD),  # plain (unescaped) text
                        host=props.get(app_constants.APP_LOCAL_DB_HOST),
                        database=props.get(app_constants.APP_LOCAL_DB_NAME),
            )
            self._initialized=True
            print("Initialized SQL DB-Pool.")
        pass
        self.engin =create_engine(url=url)
        pass
    def executeQuery(self , query:str):
        connection = None
        try:
            # connection = self.pool.getconn()
            return pandas.read_sql(query , self.engin).to_json(orient='records', indent=4)
        except Exception as ex:
            print(f"Exception while executing query:  {query} \n Error: {ex}")
        pass