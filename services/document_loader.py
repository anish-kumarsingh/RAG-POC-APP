
from datasets import load_dataset
from db import faiss_db , sql_dataset_loader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import logging 


class DocumentLoader:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, model_id:str , dimention:int):
        if not hasattr(self , '_initialized'):
            self.embedding = HuggingFaceEmbeddings(model_name=model_id)
            self.vector_db: faiss_db.FaissVectorDB = faiss_db.FaissVectorDB(embeddings=self.embedding, dimention=dimention)
            self._initialized=True
            self.logger=logging.getLogger(__name__)
            self.logger.info("Initialized Documnet Loader.")
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
        self.logger.info('Loading of data is completed...')
    
    def loadDataSetFromCsv(self , paths:list[str]):
        documents=[]
        for path in paths:
            loader=sql_dataset_loader.SqlDataSetLoader(path=path)
            dataFrame=loader.getDataFrame()
        
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
        self.logger.info(f'Loading of data is completed, total loaded documents:{len(documents)}')


            

