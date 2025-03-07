from fastapi import APIRouter

from router.routes import index_route, records_route, chat_route

api_router = APIRouter()

api_router.include_router(index_route.router, tags=["Index"])
api_router.include_router(chat_route.router, prefix="/api", tags=["Index"])
api_router.include_router(records_route.router, prefix="/api", tags=["Records"])