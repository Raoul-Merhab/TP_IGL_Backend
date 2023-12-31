from fastapi import APIRouter, status, Depends
from validators.Moderateur import *
from controllers.ModController import ModController
from utils.HTTPResponse import HTTPResponse
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()
    
@router.get("/")
def read_root():
    raise HTTPResponse(status_code=status.HTTP_200_OK,detail="Guerrout Mod")

@router.post("/rectifier-article")
def handle_rectifier_article(user : Mod_Rectifier_Article, db : Session = Depends(get_db)):
    ModController.rectifier_article(db, user.token, user.ID_article, user.titre, user.texte, user.resume, user.date_publication)

@router.post("/supprimer-article")
def handle_supprimer_article(user : Mod_Supprimer_Article, db : Session = Depends(get_db)):
    ModController.supprimer_article(db, user.token, user.ID_article)

@router.post("/valider-article")
def handle_valider_article(user : Mod_Valider_Article, db : Session = Depends(get_db)):
    ModController.valider_article(db, user.token, user.ID_article)