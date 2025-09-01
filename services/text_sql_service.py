from retriever import retriever
from gens import gen
from services import prompt_gen_service 
from langchain_core.documents import Document
import logging

class TextSqlService:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, model_id:str, llm_model:str, dimention:int, prompt_file_path:str):
        if not hasattr(self , '_initialized'):
            self.retriver = retriever.Retriver(model_id=model_id, dimention=dimention)
            self.promp_service=prompt_gen_service.PromptGenService(prompt_file_path)
            self.gen_service=gen.GeneratorService(model_id=llm_model)
            self._initialized=True
            self.logger = logging.getLogger(__name__)
            self.logger.info("Initialized text-to-sql service.")
        pass
    def askQuery(self, input_query:str)->str:
        try:
            documents:list[Document] = self.retriver.retrieveDocuments(input_query)
            instruction_prompt = self.promp_service.generatePrompt(input_query,documents)
            return self.gen_service.generateResponse(input_query, instruction_prompt).content
        except Exception as ex: 
            self.logger.info('Exception while processing requst', ex)
            pass
        return 'Unable to process your request at this moment.'
    def generateChartConfig(self, headers:dict)-> dict:
        instruction_prompt = self.promp_service.generatePrompt(input_query,documents)

