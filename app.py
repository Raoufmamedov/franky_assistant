from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from knowledge_base import KnowledgeBase
# from langchain_openai import OpenAIEmbeddings
import os


app = FastAPI()
kb = KnowledgeBase()

class QueryRequest(BaseModel):
    query: str

@app.post("/upload/")
async def upload_file(file: UploadFile):
    file_location = f"data/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"info": f"File '{file.filename}' uploaded successfully."}

@app.post("/train/")
def train_knowledge_base():
    kb.build_index("data")
    return {"info": "Knowledge base trained successfully."}

@app.post("/query/")
def query_knowledge_base(request: QueryRequest):
    results = kb.query(request.query)
    return {"results": [result.page_content for result in results]}
