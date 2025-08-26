from retriever import retriever
from gens import gen
from services import prompt_gen_service 
from langchain_core.documents import Document

class TextSqlService:
    def __init__(self, model_id:str, llm_model:str):
        self.retriver = retriever.Retriver(model_id=model_id)
        self.promp_service=prompt_gen_service.PromptGenService()
        self.gen_service=gen.GeneratorService(model_id=llm_model)
        
    def askQuery(self, input_query:str)->str:
        try:
            documents:list[Document] = self.retriver.retrieveDocuments(input_query)
            print(documents)
            instruction_prompt = self.promp_service.generatePrompt(input_query,documents)
            return self.gen_service.generateResponse(input_query, instruction_prompt).content
        except Exception as ex: 
            print('Exception while processing requst', ex)
            pass
        return 'Unable to process your request at this moment.'

