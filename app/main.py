from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello FastAPI!"}

@app.get("/api")
def hello():
    return {"message": "Hello API!"}