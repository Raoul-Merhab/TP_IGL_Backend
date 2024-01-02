from sqlalchemy.orm import Session
from fastapi import status
from models.Article import Article
from models.Auteur import Auteur
from models.Institution import Institution
from models.Mot_Cle import Mot_Cle
from models.Reference import Reference
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
    
    # Done | Not Tested
    def rectifier_article_titre_texte_resume_datePub(db : Session, token : str, ID_article : int, titre : str = None, texte : str = None, resume : str = None, date_publication : str = None):
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
    
    # Done | Not Tested
    def rectifier_article_auteur(db : Session, token : str, ID_article : int, ID_auteur : int, nom_auteur : str = None, email_auteur : str = None, ID_institution : int = None, nom_istitution : str = None, adresse_institution : str = None):
        is_mod(token=token)
        article = db.query(Article).where(Article.ID_Article == ID_article).first()
        if (not article):
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article non trouvé")
        else:
            auteur = db.query(Auteur).where(Auteur.ID_Auteur == ID_auteur).first()
            new_auteur = Auteur(Nom=auteur.Nom, Email=auteur.Email, ID_Institution=auteur.ID_Institution)
            # Rectifier nom de l'auteur
            if (nom_auteur):
                new_auteur.Nom = nom_auteur
            # Rectifier email de l'auteur
            if (email_auteur):
                new_auteur.Email = email_auteur
            # Rectifier institution de l'auteur
            if (ID_institution):
                institution = db.query(Institution).where(Institution.ID_Institution == ID_institution).first()
                new_institution = Institution(Nom=institution.Nom, Adresse=institution.Adresse)
                if (nom_istitution):
                    new_institution.Nom = nom_istitution
                if (adresse_institution):
                    new_institution.Adresse = adresse_institution
                db.add(new_institution)
                db.commit()
                db.refresh(new_institution)
                new_auteur.ID_Institution = new_institution.ID_Institution
            db.add(new_auteur)
            db.commit()
            db.refresh(new_auteur)
            index = -1
            for auteur in article.Auteurs:
                if (auteur.ID_Auteur == ID_auteur):
                    break
                index += 1
            if (index == -1):
                raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Auteur n'appartenant pas à l'article")
            article.Auteurs.pop(index)
            article.Auteurs.append(new_auteur)
            db.query(update(Article).where(Article.ID_Article == ID_article).values(Auteurs=article.Auteurs))
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Auteur de l'article rectifié")
    
    # Done | Not Tested    
    def rectifier_article_mot_cle(db : Session, token : str, ID_article : int, ID_mot_cle : int, mot_cle : str):
        is_mod(token=token)
        article = db.query(Article).where(Article.ID_Article == ID_article).first()
        if (not article):
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article non trouvé")
        else:
            new_mot_cle = Mot_Cle(Mot_Cle=mot_cle)
            db.add(new_mot_cle)
            db.commit()
            db.refresh(new_mot_cle)
            index = -1
            for mot_cle in article.Mots_Cles:
                if (mot_cle.ID_Mot_Cle == ID_mot_cle):
                    break
                index += 1
            if (index == -1):
                raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Mot clé n'appartenant pas à l'article")
            article.Mots_Cles.pop(index)
            article.Mots_Cles.append(new_mot_cle)
            db.query(update(Article).where(Article.ID_Article == ID_article).values(Mots_Cles=article.Mots_Cles))
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Mot clé de l'article rectifié")
    
    # Done | Not Tested
    def rectifier_article_reference(db : Session, token : str, ID_article : int, ID_reference : int, reference : str):
        is_mod(token=token)
        article = db.query(Article).where(Article.ID_Article == ID_article).first()
        if (not article):
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article non trouvé")
        else:
            new_reference = Reference(Reference=Reference)
            db.add(new_reference)
            db.commit()
            db.refresh(new_reference)
            index = -1
            for reference in article.References:
                if (reference.ID_Reference == ID_reference):
                    break
                index += 1
            if (index == -1):
                raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Référence n'appartenant pas à l'article")
            article.References.pop(index)
            article.References.append(reference)
            db.query(update(Article).where(Article.ID_Article == ID_article).values(References=article.References))
            db.commit()
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Référence de l'article rectifié")

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
    