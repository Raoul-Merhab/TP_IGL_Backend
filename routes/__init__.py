from fastapi import APIRouter
from routes.Authentification import router as auth_router
from routes.Administrateur import router as admin_router
from routes.Moderateur import router as mod_router

router = APIRouter()

router.include_router(router=auth_router, prefix="/auth", tags=["Authentification"])
router.include_router(router=admin_router, prefix="/admin", tags=["Administrateur"])
router.include_router(router=mod_router, prefix="/mod", tags=["Moderateur"])