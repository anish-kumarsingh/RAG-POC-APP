import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from uuid import uuid4

class FaissVectorDB:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, embeddings, dimention:int):
        if not hasattr(self , '_initialized'):
            self.__vector_store__ = FAISS(
                embedding_function=embeddings,
                index=faiss.IndexFlatL2(len(embeddings.embed_query("hello world"))),
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
            self._initialized=True
            print("Initialized Faiss DB.")
        pass

    def getDataBase(self):
        return self.__vector_store__
    def storeDocuments(self , documents: list[Document]):
        self.__vector_store__.add_documents(documents=documents , ids=self.genUUIDs(documents))
        pass
    def genUUIDs(self , documents : list[Document])->list[str]:
        return [str(uuid4()) for _ in range(len(documents))]
    def findDocuments(self , input_query:str)->list[Document]:
        return self.__vector_store__.similarity_search(input_query , k= 3)
    


