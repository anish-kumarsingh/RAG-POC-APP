# from fastapi import FastAPI
from services import text_sql_service
from services import document_loader
import os
from props import app_props
from utility import app_constants



app_properties = app_props.PropLoader('app.properties')
print(f"Hugging face key : {app_properties.getProp(app_constants.HUGGINGFACE_TOEKN_KEY)}")
#Add your tocket in environment or here so it will be available to connect with Hugging face.
os.environ.setdefault(app_properties.getProp(app_constants.HUGGINGFACE_TOEKN_KEY), app_properties.getProp(app_constants.HUGGINGFACE_TOEKN_KEY))

# app = FastAPI()

embedding_model_name=app_properties.getProp(app_constants.APP_EMBD_MODEL_ID)

llm_model = app_properties.getProp(app_constants.APP_LLM_MODEL_ID)

doc_loader = document_loader.DocumentLoader(model_id=embedding_model_name, dimention=768)

doc_loader.loadDataSetFromCsv('text-sql-dataset.csv')

rag = text_sql_service.TextSqlService(embedding_model_name, llm_model=llm_model)


# @app.get("/text-sql")
def processAgentRequst(input_query:str)-> str:
    return rag.askQuery(input_query=input_query)
