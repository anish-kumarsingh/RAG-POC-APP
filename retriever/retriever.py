from db import faiss_db
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class Retriver:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self , model_id:str, dimention:int):
        if not hasattr(self , '_initialized'):
            self.embedings=HuggingFaceEmbeddings(model_name=model_id)
            self.vector_db:faiss_db.FaissVectorDB = faiss_db.FaissVectorDB(self.embedings, dimention)
        pass
    def retrieveDocuments(self , input_query:str)-> list[Document]:
        return self.vector_db.findDocuments(input_query)
