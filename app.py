
from services import text_sql_service
from services import document_loader
from utility import app_constants
from configs import config
from db import local_db as dao
import logging

class App:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self , '_initialized'):
            self.app_config=config.AppConfig()
            self.embedding_model_name=self.app_config.get(app_constants.APP_EMBD_MODEL_ID)
            self.llm_model = self.app_config.get(app_constants.APP_LLM_MODEL_ID)
            self.dimention=self.app_config.get(app_constants.APP_VECTOR_DB_DIMEN)
            self.doc_loader = document_loader.DocumentLoader(model_id=self.embedding_model_name, dimention=self.dimention)
            self.doc_loader.loadDataSetFromCsv(self.app_config.get(app_constants.APP_VECTOR_DB_SAMPLE_DATASET))
            self.sql_gen = text_sql_service.TextSqlService(self.embedding_model_name, llm_model=self.llm_model, dimention=self.dimention, prompt_file_path=self.app_config.get(app_constants.APP_PROMPT_FILE))
            self.dao=dao.SqlDataPool(self.app_config)
            self._initialized=True
            self.logger= logging.getLogger(__name__)
            self.logger.info("App initialization completed.")
        pass
    def generateSql(self , input_query: str)-> str:
        return self.sql_gen.askQuery(input_query=input_query)
    def executeSql(self , sql_query:str):
        return { 'data': self.dao.executeQuery(sql_query),
                  'chart-configs' : self.sql_gen.askQuery(input_query=input_query) }

