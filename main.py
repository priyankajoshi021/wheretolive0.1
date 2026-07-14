
from fastapi import FastAPI

app =  FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to the wheretolive 1.0"}






























