from fastapi import FastAPI, Request
import app
from time import perf_counter 
import logging 


logging.basicConfig(
    level=logging.INFO,
    format=' %(asctime)s - %(name)s - %(levelname)s : %(message)s '
)

logger=logging.getLogger(__name__)

fastApp = FastAPI()

rag = app.App()

@fastApp.get("/generate-sql")
def generate_sql(query:str)->str:
    return rag.generateSql(query)

def executeSql(query:str):
    return rag.executeSql(query)

@fastApp.middleware('http')
async def requestLogger(request : Request, chain):
    start_time = perf_counter()
    response = await chain(request)
    duration = perf_counter() - start_time
    logger.info(
        '[metric:call.duration] %s %s %d - %.2fs',
        request.method, request.url, response.status_code , duration
    )
    return response


