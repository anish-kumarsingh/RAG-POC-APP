
from services import text_sql_service
from services import document_loader
from utility import app_constants
from configs import config
from db import local_db as dao
import logging
from services import prompt_gen_service
from gens import gen
import pandas

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
            self.promp_service=prompt_gen_service.PromptGenService(prompt_file=self.app_config.get(app_constants.APP_PROMPT_FILE), chart_prompt_file=self.app_config.get(app_constants.CHART_PROMPT_FILE),sys_chart_prompt_file=self.app_config.get(app_constants.SYS_CHART_APP_PROMPT_FILE))
            self.sql_gen = text_sql_service.TextSqlService(self.embedding_model_name, llm_model=self.llm_model, dimention=self.dimention, prompt_file_path=self.app_config.get(app_constants.APP_PROMPT_FILE), chart_prompt_file=self.app_config.get(app_constants.APP_PROMPT_FILE), system_chart_prompt_file=self.app_config.get(app_constants.SYS_CHART_APP_PROMPT_FILE))
            self.gen_service=gen.GeneratorService(model_id=self.llm_model)
            self.dao=dao.SqlDataPool(self.app_config)
            self._initialized=True
            self.logger= logging.getLogger(__name__)
            self.logger.info("App initialization completed.")
        pass
    def generateSql(self , input_query: str)-> str:
        return self.sql_gen.askQuery(input_query=input_query)
    def executeSql(self , sql_query:str):
        dataFrame:pandas.DataFrame=self.dao.executeQuery(sql_query)
        return { 'data': dataFrame.to_json(index=4),
                  'chart-configs' : self.gen_service.generateResponse(input_query=self.promp_service.prepareChartPromt(dataFrame.columns.tolist()), instruction_prompt=self.promp_service.getSystemChartPrompt()) 
                }

