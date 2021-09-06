__version__ = '0.1.0'


from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "Pong!!!"}
