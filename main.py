from fastapi import FastAPI
from services import text_sql_service
from services import document_loader
import os

#Add your tocket in environment or here so it will be available to connect with Hugging face.
os.environ.setdefault("HF_TOKEN", "XXXXXXXXXX")

app = FastAPI()

embedding_model_name="all-MiniLM-L6-v2"

llm_model = "meta-llama/Meta-Llama-3-8B-Instruct"

doc_loader = document_loader.DocumentLoader(model_id=embedding_model_name, dimention=768)
doc_loader.loadDataSet()

rag = text_sql_service.TextSqlService(embedding_model_name, llm_model=llm_model)


@app.get("/text-sql")
async def processAgentRequst(input_query:str)-> str:
    return rag.askQuery(input_query=input_query)
