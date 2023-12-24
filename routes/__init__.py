from fastapi import APIRouter
from routes.Administrateur import router as admin_router
from routes.Auth import router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["Authentification"])