from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Init": "First API with FastAPI!"}
