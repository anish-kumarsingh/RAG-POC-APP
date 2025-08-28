from db import faiss_db
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class Retriver:
    def __init__(self , model_id:str):
        self.embedings=HuggingFaceEmbeddings(model_name=model_id)
        self.vector_db:faiss_db.FaissVectorDB = faiss_db.FaissVectorDB(self.embedings, 768)
        pass
    def retrieveDocuments(self , input_query:str)-> list[Document]:
        return self.vector_db.findDocuments(input_query)
