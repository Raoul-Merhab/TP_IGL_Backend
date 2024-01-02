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
    if (user.mot_cle):
        ModController.rectifier_article_mot_cle(db, user.token, user.ID_article, user.mot_cle.ID_mot_cle, user.mot_cle.mot_cle)
    elif (user.reference):
        ModController.rectifier_article_reference(db, user.token, user.ID_article, user.reference.ID_reference, user.reference.reference)
    elif (user.auteur):
        ModController.rectifier_article_auteur(db, user.token, user.ID_article, user.auteur.ID_auteur, user.auteur.nom_auteur, user.auteur.email_auteur, user.auteur.institution.ID_institution, user.auteur.institution.nom_institution, user.auteur.institution.adresse_institution)
    elif (user.titre or user.texte or user.resume or user.date_publication):
        ModController.rectifier_article_titre_texte_resume_datePub(db, user.token, user.ID_article, user.titre, user.texte, user.resume, user.date_publication)
    else:
        raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Aucun champ à rectifier specifié")

@router.post("/supprimer-article")
def handle_supprimer_article(user : Mod_Supprimer_Article, db : Session = Depends(get_db)):
    ModController.supprimer_article(db, user.token, user.ID_article)

@router.post("/valider-article")
def handle_valider_article(user : Mod_Valider_Article, db : Session = Depends(get_db)):
    ModController.valider_article(db, user.token, user.ID_article)