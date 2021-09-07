__version__ = '0.1.0'


from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
import uvicorn

app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/ping")
async def ping():
    return {"message": "Pong!!!"}


@app.get("/token")
async def get_token(token: str = Depends(oauth_scheme)):
    return {"token": token}


def run_dev_server():
    uvicorn.run("sliya:app", host="localhost", port=9715, log_level="debug")
