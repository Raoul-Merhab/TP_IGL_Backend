from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db 
from models import Article_Favori


def addToFavorites(article_id: int, utilisateur_id: int, db: Session = Depends(get_db)):
    nouvel_article_favori = Article_Favori(ID_Article=article_id, ID_Compte=utilisateur_id)
    db.add(nouvel_article_favori)
    db.commit()
    # db.refresh(nouvel_article_favori)
    return None

def getFavorites(utilisateur_id: int, db: Session = Depends(get_db)):
    favoris = db.query(Article_Favori).filter(Article_Favori.ID_Compte == utilisateur_id).all()
    return favoris

def deleteFavorites(article_id: int, utilisateur_id:int, db: Session = Depends(get_db)):
    fav_to_delete = db.query(Article_Favori).filter(Article_Favori.ID_Article == article_id,Article_Favori.ID_Compte == utilisateur_id).first()
    if fav_to_delete:
        db.delete(fav_to_delete)
        db.commit()
        return None
    raise HTTPException(status_code=404, detail="article favori non trouvé")
    