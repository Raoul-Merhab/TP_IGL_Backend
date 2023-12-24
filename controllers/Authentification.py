from database import get_db
from fastapi import Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import update
from models.Administrateur import Administrateur
from models.Moderateur import Moderateur
from models.Utilisateur import Utilisateur
from utils.Auth import generate_token, check_token, Token_Payload
from utils.Role import Role
from typing import Optional
from utils.HTTPResponse import HTTPResponse

class Authentification():
    
    # Done
    def get_profile(token : str, db: Session = Depends(get_db)):
        checked_token = check_token(token=token)
        if (not checked_token):
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
        
        if (checked_token.get_role() == Role.ADMIN):
            result = db.query(Administrateur).filter(Administrateur.ID_Administrateur == checked_token.get_id()).first()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "nom": result.Nom,
                    "email": result.Email,
                    "role": checked_token.role.value
                }
            )
        elif (checked_token.get_role() == Role.MOD):
            result = db.query(Moderateur).filter(Moderateur.ID_Moderateur == checked_token.get_id()).first()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "nom": result.Nom,
                    "email": result.Email,
                    "role": checked_token.role.value
                }
            )
        elif (checked_token.get_role() == Role.USER):
            result = db.query(Utilisateur).filter(Utilisateur.ID_Utilisateur == checked_token.get_id()).first()
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "nom": result.Nom,
                    "email": result.Email,
                    "role": checked_token.role.value
                }
            )
        raise HTTPResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")
    
    # Done
    def edit_profile(token : str, nom : Optional[str] , email : Optional[str], password : Optional[str], db: Session = Depends(get_db)):
        checked_token = check_token(token=token)
        if (not checked_token):
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
        if (checked_token.get_role() == Role.ADMIN):
            admin = db.query(Administrateur).filter(Administrateur.ID_Administrateur == checked_token.get_id()).first()
            if ( nom is not None):
                admin.Nom = nom
            if ( email is not None):
                admin.Email = email
            if ( password is not None):
                # reste le hachage du password
                admin.password = password
            update(Administrateur).where(Administrateur.ID_Administrateur == checked_token.get_id()).values(admin)
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "message": "Profile updated",
                    "token": generate_token(admin),
                }
            )
        elif (checked_token.get_role() == Role.MOD):
            mod = db.query(Moderateur).filter(Moderateur.ID_Moderateur == checked_token.get_id()).first()
            if ( nom is not None):
                mod.Nom = nom
            if ( email is not None):
                mod.Email = email
            if ( password is not None):
                # reste le hachage du password
                mod.password = password
            update(Moderateur).where(Moderateur.ID_Moderateur == checked_token.get_id()).values(mod)
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "message": "Profile updated",
                    "token": generate_token(mod),
                }
            )
        elif (checked_token.get_role() == Role.USER):
            user = db.query(Utilisateur).filter(Utilisateur.ID_Utilisateur == checked_token.get_id()).first()
            if ( nom is not None):
                user.Nom = nom
            if ( email is not None):
                user.Email = email
            if ( password is not None):
                # reste le hachage du password
                user.password = password
            update(Utilisateur).where(Utilisateur.ID_Utilisateur == checked_token.get_id()).values(user)
            raise HTTPResponse(
                status_code=status.HTTP_200_OK,
                detail={
                    "message": "Profile updated",
                    "token": generate_token(user),
                }
            )
        raise HTTPResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")

    # Done
    def log_in(email : str, password : str, db: Session = Depends(get_db)):
        # Search in admin
        result = db.query(Administrateur).filter(Administrateur.email == email).first()
        if (result is not None ):
            # rest le hachage du password
            password = password
            if (result.password == password ):
                # generat jwt and send token for admin
                raise HTTPResponse(
                    status_code=status.HTTP_200_OK,
                    detail={
                        "token": generate_token(result),
                        "role": Role.ADMIN.value
                    },
                )
            else:
                # error in the password
                raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
        else:
            # search in moderator
            result = db.query(Moderateur).filter(Moderateur.email == email).first()
            if (result is not None ):
                # rest le hachage du password
                if (result.password == password ):
                    # generat jwt and send token for mod
                    raise HTTPResponse(
                        status_code=status.HTTP_200_OK,
                        detail={
                            "token": generate_token(result),
                            "role": Role.MOD.value
                        },
                    )
                else:
                    # error in the password
                    raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
            else:
                # serach in Utilisateur
                result = db.query(Utilisateur).filter(Utilisateur.email == email).first()
                if (result is not None ):
                    # rest le hachage du password
                    if (result.password == password ):
                        # generat jwt and send token for user
                        raise HTTPResponse(
                            status_code=status.HTTP_200_OK,
                            detail={
                                "token": generate_token(result),
                                "role": Role.USER.value
                            },
                        )
                    else:
                        # error in the password
                        raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect password")
                else:
                    # error in the email
                    raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email adress not found")
    
    # Done
    def sign_up(email : str, password : str, nom : str, db: Session = Depends(get_db)):
        result = db.query(Administrateur).filter(Administrateur.email == email).first()
        if (result is not None ):
            raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email adress already exists")
        else:
            # search in moderator
            result = db.query(Moderateur).filter(Moderateur.email == email).first()
            if (result is not None ):
                raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email adress already exists")
            else:
                # serach in Utilisateur
                result = db.query(Utilisateur).filter(Utilisateur.email == email).first()
                if (result is not None ):
                    raise HTTPResponse(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email adress already exists")
                else:
                    # account doesn't exist, account to be created
                    # rest le hachage du password
                    password = password
                    nouveau_utilisateur = Utilisateur(nom=nom, email=email, password=password)
                    db.add(nouveau_utilisateur)
                    db.commit()
                    db.refresh(nouveau_utilisateur)
                    raise HTTPResponse(
                        status_code=status.HTTP_201_CREATED,
                        detail={
                            "token": generate_token(nouveau_utilisateur),
                            "role": Role.USER.value
                        }
                    )
                
    def a():
        pass