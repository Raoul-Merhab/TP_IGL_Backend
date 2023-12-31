from sqlalchemy.orm import Session
from fastapi import status
from models.Article import Article
from sqlalchemy import delete, update
from utils.Auth import check_token, Token_Payload
from utils.Role import Role
from utils.HTTPResponse import HTTPResponse

# Done

def is_mod (token : str) -> Token_Payload:
    checked_token = check_token(token=token)
    if (not checked_token ):
        raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expiré")
    elif (checked_token.get_role() != Role.MOD ):
        raise HTTPResponse(status_code=status.HTTP_403_FORBIDDEN,detail="Vous n'êtes pas l'accés à la section modérateur")
    return checked_token

class ModController:
    
    # Not Done | Reste les auteurs, mots clés et références
    def rectifier_article(db : Session, token : str, ID_article : int, titre : str = None, texte : str = None, resume : str = None, date_publication : str = None):
        is_mod(token=token)
        article = db.query(Article).where(Article.ID_Article == ID_article).first()
        if (not article):
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article non trouvé")
        else:
            to_update = {}
            if (titre):
                to_update["Titre"] = titre
            if (texte):
                to_update["Texte"] = texte
            if (resume):
                to_update["Resume"] = resume
            if (date_publication):
                to_update["Date_Publication"] = date_publication
            db.execute(update(Article).where(Article.ID_Article == ID_article).values(to_update))
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article rectifié")
    
    # Done | Works
    def supprimer_article(db : Session, token : str, ID_article : int):
        is_mod(token=token)
        article = db.query(Article).where(Article.ID_Article == ID_article).first()
        if (not article):
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article non trouvé")
        else:
            db.execute(delete(Article).where(Article.ID_Article == ID_article))
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article supprimé")
        
    # Done | Works
    def valider_article(db : Session, token : str, ID_article : int):
        is_mod(token=token)
        article = db.query(Article).where(Article.ID_Article == ID_article).first()
        if (not article):
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article non trouvé")
        else:
            db.execute(update(Article).where(Article.ID_Article == ID_article).values(Valide=True))
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article validé")
    