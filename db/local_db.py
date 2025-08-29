
from psycopg2 import pool
from props import app_props
from utility import app_constants
import pandas
import pandas.io.sql as sql
from sqlalchemy import create_engine, URL
sql_db_pool = None 

class SqlDataPool:
    def __init__(self, props:app_props.PropLoader):
        # global sql_db_pool
        # sql_db_pool = pool.SimpleConnectionPool(
        #         minconn=props.getProp(app_constants.APP_LOCAL_MIN_POOL_SIZE),
        #         maxconn=props.getProp(app_constants.APP_LOCAL_MAX_POOL_SIZE),
        #         user=props.getProp(app_constants.APP_LOCAL_DB_USER_NAME),
        #         password=props.getProp(app_constants.APP_LOCAL_DB_PSSWORD),
        #         host=props.getProp(app_constants.APP_LOCAL_DB_HOST), 
        #         port=props.getProp(app_constants.APP_LOCAL_DB_PORT), 
        #         database=props.getProp(app_constants.APP_LOCAL_DB_NAME)
        # )
        # self.pool=sql_db_pool
        url=URL.create(
                    "postgresql+psycopg2",
                    username=props.getProp(app_constants.APP_LOCAL_DB_USER_NAME),
                    password=props.getProp(app_constants.APP_LOCAL_DB_PSSWORD),  # plain (unescaped) text
                    host=props.getProp(app_constants.APP_LOCAL_DB_HOST),
                    database=props.getProp(app_constants.APP_LOCAL_DB_NAME),
        )
        self.engin =create_engine(url=url)
        pass
    def executeQuery(self , query:str)-> pandas.DataFrame | None:
        connection = None
        try:
            # connection = self.pool.getconn()
            return pandas.read_sql(query , self.engin)
        except Exception as ex:
            print(f"Exception while executing query:  {query} \n Error: {ex}")
        #if connection is not None:
            # self.pool.putconn(connection)
        pass