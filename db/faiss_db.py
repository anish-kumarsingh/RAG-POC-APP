import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from uuid import uuid4

__vector_store__ : FAISS = None

class FaissVectorDB:
    def __init__(self, embeddings, dimention:int):
        global __vector_store__
        if __vector_store__ is None:
            __vector_store__ = FAISS(
                embedding_function=embeddings,
                index=faiss.IndexFlatL2(len(embeddings.embed_query("hello world"))),
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )

    def getDataBase(self):
        global __vector_store__
        return __vector_store__
    def storeDocuments(self , documents: list[Document]):
        global __vector_store__
        __vector_store__.add_documents(documents=documents , ids=self.genUUIDs(documents))
        pass
    def genUUIDs(self , documents : list[Document])->list[str]:
        return [str(uuid4()) for _ in range(len(documents))]
    def findDocuments(self , input_query:str)->list[Document]:
        global __vector_store__
        return __vector_store__.similarity_search(input_query , k= 2)
    


