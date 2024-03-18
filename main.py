from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print("start")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, texte: str):

    return {"texte": texte, "filename": file.filename}


@app.post("/contextText/")
async def create_upload_file(context: str, texte: str):

    return {"texte": texte, "context": context}


@app.post("/withoutFile/")
async def create_upload_file(texte: str):

    return {"texte": texte}


def extract_data(file: UploadFile) -> Union[str, dict, list]:
    if file.filename.endswith(".txt"):
        data = file.file.read()
        return data.decode("utf-8")
    elif file.filename.endswith(".csv"):
        data = file.file.read().decode("utf-8")
        rows = data.split("\n")
        reader = csv.DictReader(rows)
        return [dict(row) for row in reader]
    elif file.filename.endswith(".json"):
        data = file.file.read().decode("utf-8")
        return json.loads(data)
    else:
        return "Invalid file format"
