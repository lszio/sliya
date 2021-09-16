from fastapi import APIRouter
from sliya.api import ping, user

router = APIRouter()

router.include_router(ping.router)
router.include_router(user.router, prefix="/user")
