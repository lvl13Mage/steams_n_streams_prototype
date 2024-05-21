from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from api.middleware import DBSessionMiddleware
from api.routes.player import router as player_router
from api.routes.community import router as community_router
from api.routes.debug import router as debug_router
from api.routes.node import router as node_router

app = FastAPI()

app.add_middleware(DBSessionMiddleware)

api_router = APIRouter()
api_router.include_router(debug_router)
api_router.include_router(player_router)
api_router.include_router(community_router)
api_router.include_router(node_router)

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(api_router)