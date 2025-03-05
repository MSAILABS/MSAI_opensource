from fastapi import APIRouter

from router.routes import index_route

api_router = APIRouter()

api_router.include_router(index_route.router, tags=["Index"])