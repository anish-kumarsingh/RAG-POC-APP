from langchain_core.documents import Document
from services import file_service
import logging

class PromptGenService:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, prompt_file:str):
        if not hasattr(self , '_initialized'):
            self.file_service=file_service.FileService()
            self.template=self.file_service.loadTextFile(prompt_file)
            self._initialized=True
            self.logger = logging.getLogger(__name__)
            self.logger.info("Initialized Prompt Gen.")
        pass
    def generatePrompt(self , input_query : str , documents: list[Document])->str:
        return self.__prepareContext__(input_query , documents)
    def __prepareContext__(self , input_query:str , documents : list[Document])->str:
        prompt = self.template.replace('__db_schema_definition__',documents[0].metadata['schema_context']).replace('__examples__','\n'.join([f' - {self.prep_doc(doc)}' for doc in documents])).replace('__input_query__', input_query)
        self.logger.info('[Instruction Prompt] : $s', prompt)
        return prompt
    def __prepDocumentContext__(self , docuemnt:Document)->str:
        return (
            f"Example: {docuemnt.metadata['prompt']}\n"
            f"Sql Query: {docuemnt.metadata['sql_query']}\n"
        )
    def prep_doc(self , item:Document):
        return (
                f"Example: {item.metadata['prompt']}\n"
                f"Sql Query: {item.metadata['sql_query']}\n"
            )
    def prepareChartPromt(self , headers:dict):
        