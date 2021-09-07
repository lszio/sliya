__version__ = '0.1.0'

from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import uvicorn

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 63

app = FastAPI()

fake_users = {
    "admin": {
        "username": "admin",
        "email": "",
        "nickname": "gly",
        "password": "$2a$10$tCL8F5Yha5gtIvwA5hIykeVrB/vHMD8gqNw303tFdiDQ1gkdiS1/K"
    },
    "liszt": {
        "username": "liszt",
        "email": "liszt21@qq.vom",
        "password": "$2a$10$qX9yfE06Igf.YD4bP/2OLeIcsQbmtSCTt1JIHxHPohQN2hUEqlfIS",
        "nickname": "me"
    }
}

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    disabled: bool = False


class Token(BaseModel):
    token: str
    type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(User):
    password: str


def fake_decode_token(token):
    return User(
        username=token, email="liszt21@qq.com", nickname="Liszt21"
    )


crypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verigy_password(raw, decoded):
    return crypt_context.verify(raw, decoded)


def decode_password(password):
    return crypt_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user = db[username]
        return UserInDB(**user)


@app.get("/ping")
async def ping():
    return {"message": "Pong!!!"}


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verigy_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="not valid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        fake_users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"token": access_token, "type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


def run_dev_server():
    uvicorn.run("sliya:app", host="localhost",
                port=9715, log_level="debug", debug=True)
