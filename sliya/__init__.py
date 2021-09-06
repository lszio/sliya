__version__ = '0.1.0'


from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"message": "Pong!!!"}

def run_dev_server():
    uvicorn.run("sliya:app", host="localhost", port=9715, log_level="debug")
