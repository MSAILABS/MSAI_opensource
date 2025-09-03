from fastapi import APIRouter

from api.routes import index_route, record_route, sse_route, chat_route, cluster_route

api_router = APIRouter()

api_router.include_router(index_route.router, tags=["Index"])
api_router.include_router(chat_route.router, prefix="/api", tags=["Chat"])
api_router.include_router(record_route.router, prefix="/api", tags=["Records"])
api_router.include_router(cluster_route.router, prefix="/api", tags=["Clusters"])
api_router.include_router(sse_route.router, prefix="/api", tags=["Server Side Events"])