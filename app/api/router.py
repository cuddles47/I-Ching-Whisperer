from fastapi import APIRouter

from app.api.endpoints import divination

api_router = APIRouter()

# Include endpoints from different modules
api_router.include_router(divination.router, prefix="/divination", tags=["divination"])
