from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile 
from typing import Union 
import json 
import csv
from modeles import bert, squeezebert, deberta
from uploadFile import file_to_text
from typing import List
from transformers import pipeline
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Request(BaseModel):
    context: str
    question: str
    model: Optional[str] = None
    # files: Optional[List[UploadFile]] = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipSqueezeBert = pipeline("question-answering", model="ALOQAS/squeezebert-uncased-finetuned-squad-v2")
pipBert = pipeline('question-answering', model="ALOQAS/bert-large-uncased-finetuned-squad-v2")
pipDeberta = pipeline('question-answering', model="ALOQAS/deberta-large-finetuned-squad-v2")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/contextText/")
async def create_upload_file(request: Request):
    try:
        if request.model == "squeezebert":
            answer = squeezebert(request.context, request.question, pipSqueezeBert)
        elif request.model == "bert":
            answer = bert(request.context, request.question, pipBert)
        elif request.model == "deberta":
            answer = deberta(request.context, request.question, pipDeberta)
        else:
            raise HTTPException(status_code=400, detail="Model not found.")
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/uploadfile/")
async def create_upload_file(files: List[UploadFile] = File(...), question: str = Form(...), model: str = Form(...)):
    res = ""
    for file in files:
        try:
            res += await file_to_text(file)
        except Exception as e:
            print(f"Failed to process file {file.filename}: {e}") 
            continue 

    if res == "":
        raise HTTPException(status_code=400, detail="All files failed to process.")
    
    answer = None
    if model == "squeezebert":
        answer = squeezebert(res, question, pipSqueezeBert)
    elif model == "bert":
        answer = bert(res, question, pipBert)
    elif model == "deberta":
        answer = deberta(res, question, pipDeberta)
    else:
        raise HTTPException(status_code=400, detail="Model not found.")
    
    return answer

@app.post("/squeezebert/")
async def qasqueezebert(request: Request):
    try:
        squeezebert_answer = squeezebert(request.context, request.question, pipSqueezeBert)
        if squeezebert_answer:
            return squeezebert_answer
        else:
            raise HTTPException(status_code=404, detail="No answer found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/bert/")
async def qabert(request: Request):
    try:
        bert_answer = bert(request.context, request.question, pipBert)
        if bert_answer:
            return bert_answer
        else:
            raise HTTPException(status_code=404, detail="No answer found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/deberta/")
async def qadeberta(request: Request):
    try:
        deberta_answer = deberta(request.context, request.question, pipDeberta)
        if deberta_answer:
            return deberta_answer
        else:
            raise HTTPException(status_code=404, detail="No answer found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
