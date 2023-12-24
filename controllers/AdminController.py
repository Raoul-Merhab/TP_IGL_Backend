import requests
from sqlalchemy.orm import Session
from fastapi import Depends, status
from database import get_db, get_next_id
from models.Article import Article
from models.Moderateur import Moderateur
from sqlalchemy import insert, delete
from utils.Auth import check_token, Token_Payload
from utils.Role import Role
from utils.HTTPResponse import HTTPResponse
from utils import get_file_path

class AdminController():
    
    # Done
    def is_admin (token : str) -> Token_Payload:
        checked_token = check_token(token=token)
        if (not checked_token ):
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        elif (checked_token.get_role() != Role.ADMIN ):
            raise HTTPResponse(status_code=status.HTTP_403_FORBIDDEN,detail="You don't have access to this section")
        return checked_token
    
    # Done
    def upload_article (self,  token : str, link : str, db: Session = Depends(get_db) ):
        checked_token = self.is_admin(token=token, db=db)
        data = requests.api.get(url=link)
        if (data.headers.get('content-type') == "application/pdf" ): # is PDF file
            # get next ID
            ID = get_next_id(Article.__tablename__, "ID_Article", db) 
            # write the file
            file_name = get_file_path(ID)
            file = open(file_name,'wb')
            file.write(data.content)
            file.close()
            # truc traitement
            titre = ''
            texte = ''
            resume = ''
            date = ''
            # insert in the database
            nouveau_article = Article(Texte=texte, Resume=resume, Titre=titre, Valide=False, Date_Publication=date)
            db.add(nouveau_article)
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK,detail="Success")
        else: # is not PDF file
            raise HTTPResponse(status_code=status.HTTP_400_BAD_REQUEST,detail="Not a PDF file")
        
    # Done
    def ajouter_moderateur(self, token : str, nom : str, email : str, password : str, db: Session = Depends(get_db) ):
        checked_token = self.is_admin(token=token, db=db)
        nouveau_moderateur = Moderateur(Nom=nom, Email=email, Password=password, ID_Admin_Valide=checked_token.get_id())
        db.add(nouveau_moderateur)
        db.commit()
        raise HTTPResponse(status_code=status.HTTP_200_OK,detail="Success")

    # Done
    def supprimer_moderateur(self, token : str, ID_mod : int, db: Session = Depends(get_db) ):
        checked_token = self.is_admin(token=token)
        mod = db.query(Moderateur).where(Moderateur.ID_Moderateur == ID_mod).first()
        if ( mod.ID_Admin_Valide == checked_token.id ):
            db.delete(mod)
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Moderateur deleted successfully")
        else:
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED, detail="Impossible de supprimer un moderateur que vous n'avez pas validé")

    # Done
    def moderateurs(self, token : str, db: Session = Depends(get_db) ):
        self.is_admin(token=token)
        result = db.query(Moderateur).all()
        raise HTTPResponse(
            status_code=status.HTTP_200_OK,
            detail=result
        )

