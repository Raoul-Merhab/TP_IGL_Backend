from fastapi import APIRouter, status
from validators.Administrateur import *
from controllers.AdminController import AdminController
from utils.HTTPResponse import HTTPResponse

router = APIRouter()
    
@router.get("/")
def read_root():
    raise HTTPResponse(status_code=status.HTTP_200_OK,detail="Guerrout Admin")

@router.post("/upload_article")
def handle_upload_article(user : Admin_Upload_Article ):
    AdminController.upload_article(user.token, user.link)

@router.post("/ajouter_moderateur")
def handle_upload_article(user : Admin_Ajouter_Moderateur ):
    AdminController.ajouter_moderateur(user.token, user.nom, user.email, user.password)

@router.post("/supprimer_moderateur")
def handle_upload_article(user : Admin_Supprimer_Moderateur ):
    AdminController.supprimer_moderateur(user.token, user.ID_Moderateur)

@router.get("/liste_des_moderateurs")
def handle_liste_des_moderateurs(user : Admin):
    AdminController.moderateurs(user.token)

