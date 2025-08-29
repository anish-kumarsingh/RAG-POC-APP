
from datasets import load_dataset
from db import faiss_db , sql_dataset_loader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class DocumentLoader:
    def __init__(self, model_id:str , dimention:int):
        embedding = HuggingFaceEmbeddings(model_name=model_id)
        self.vector_db: faiss_db.FaissVectorDB = faiss_db.FaissVectorDB(embeddings=embedding, dimention=dimention)
        pass
    def loadDataSet(self):
        dataset=load_dataset("gretelai/synthetic_text_to_sql", split="train[:1000]")
        documents=[]
        for item in dataset:
            doc_text = (
                f"Question: {item['sql_prompt']}\n"
                f"Database Schema: {item['sql_context']}"
            )
            metadata = {
                "prompt": item['sql_prompt'],
                "schema_context": item['sql_context'],
                "sql_query": item['sql'], # Storing the actual SQL query as well
                "domain": item['domain']
            }
            documents.append(Document(page_content=doc_text, metadata=metadata))
        self.vector_db.storeDocuments(documents)
        print('Loading of data is completed...')
    
    def loadDataSetFromCsv(self , path:str):
        loader=sql_dataset_loader.SqlDataSetLoader(path=path)
        dataFrame=loader.getDataFrame()
        documents=[]
        for index , item in dataFrame.iterrows():
            doc_text = (
                f"Question: {item['sql_prompt']}\n"
                f"Database Schema: {item['sql_context']}"
            )
            metadata = {
                "prompt": item['sql_prompt'],
                "schema_context": item['sql_context'],
                "sql_query": item['sql'], # Storing the actual SQL query as well
                "domain": item['domain']
            }
            documents.append(Document(page_content=doc_text, metadata=metadata))
        self.vector_db.storeDocuments(documents)
        print('Loading of data is completed...')

