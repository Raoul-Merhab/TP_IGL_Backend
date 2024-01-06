import logging
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db 
from models import Article_Favori
from utils.HTTPResponse import HTTPResponse

class Article_Favori():

    def addToFavorites(article_id: int, utilisateur_id: int, db: Session = Depends(get_db)):
      try:
            # check if the article exists in the database
         existing_favorite = db.query(Article_Favori).filter(
         Article_Favori.ID_Article == article_id,
         Article_Favori.ID_Compte == utilisateur_id
            ).first()

         if existing_favorite:
                # Article is already in favorites
                response_body = {"message": "Article already in favorites"}
                return JSONResponse(content=response_body, status_code=200)

         else: 
             # Article is not in favorites, add it 
             nouvel_article_favori = Article_Favori(ID_Article=article_id, ID_Compte=utilisateur_id)
             db.add(nouvel_article_favori)
             db.commit()
             db.refresh(nouvel_article_favori)

             response_body = {"message": "Article ajouté aux favoris"}
             return JSONResponse(content=response_body, status_code=200)

      except Exception as e:
            logging.error(f"Error in addToFavorites: {e}")
            raise HTTPException(status_code=500, detail="article non ajoute")

    def getFavorites(utilisateur_id: int, db: Session = Depends(get_db)):
        try:
            favoris = db.query(Article_Favori).filter(Article_Favori.ID_Compte == utilisateur_id).all()
            logging.info(f"Favorites for utilisateur_id {utilisateur_id}: {favoris}")
            return favoris
        except Exception as e:
            logging.error(f"Error in getFavorites: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def deleteFavorites(article_id: int, utilisateur_id:int, db: Session = Depends(get_db)):
        fav_to_delete = db.query(Article_Favori).filter(Article_Favori.ID_Article == article_id,Article_Favori.ID_Compte == utilisateur_id).first()
        if fav_to_delete:
            db.delete(fav_to_delete)
            db.commit()
            return HTTPResponse(status_code=200, detail="article supprime")
        raise HTTPException(status_code=404, detail="article favori non trouvé")
    