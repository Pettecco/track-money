from fastapi import APIRouter

from app.authentication._register_user import register_user

user_router = APIRouter()

user_router.add_api_route(
    path="",
    endpoint=register_user,
    methods=["POST"],
    response_model=None,
    tags=["users"],
    summary="Create a new user",
)
