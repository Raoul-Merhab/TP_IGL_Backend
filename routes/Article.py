from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import Article_Favori
from database import get_db

router= APIRouter()

# Route pour ajouter un favori
@router.post("/add-favorite/")
def addToFavoritesRoute(article_id: int, utilisateur_id: int, db: Session = Depends(get_db)):
    return Article_Favori.addToFavorites(article_id, utilisateur_id, db)

# Route pour recuperer les favoris d'un utilisateur
@router.get("/get-favorite/{utilisateur_id}")
def getFavoritesRoute(utilisateur_id: int, db: Session = Depends(get_db)):
    return Article_Favori.getFavorites(utilisateur_id, db)

# Route pour supprimer les favoris
@router.delete("/delete-favorite/{utilisateur_id}/{article_id}")
def deleteFavoritesRoute(article_id: int, utilisateur_id: int, db: Session = Depends(get_db)):
    return Article_Favori.deleteFavorites(article_id, utilisateur_id, db)