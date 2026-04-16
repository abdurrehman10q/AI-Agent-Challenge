from fastapi import APIRouter
from core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}