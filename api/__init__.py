from fastapi import FastAPI, APIRouter

from api.routes.player import router as player_router

app = FastAPI()

api_router = APIRouter()
api_router.include_router(player_router)

app.include_router(api_router)