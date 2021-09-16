from fastapi import APIRouter

router = APIRouter()


@router.get("/token")
def get_user_token():
    return "token"
