from pydantic import BaseModel

class Mod(BaseModel):
    token: str

class Mod_Rectifier_Article(Mod):
    
    class Auteur_Validator(BaseModel):
    
        class Institution_Validator(BaseModel):
            ID_institution: int
            nom_institution: str = None
            adresse_institution: str = None
    
        ID_auteur: int
        nom_auteur: str = None
        email_auteur: str = None
        institution: Institution_Validator = None
    
    class Mot_Cle_Validator(BaseModel):
        ID_mot_cle: int
        mot_cle: str
    
    class Reference_Validator(BaseModel):
        ID_reference: int
        reference: str
    
    ID_article: int
    titre: str = None
    texte: str = None
    resume: str = None
    date_publication: str = None
    auteur: Auteur_Validator = None
    mot_cle: Mot_Cle_Validator = None
    reference: Reference_Validator = None


class Mod_Supprimer_Article(Mod):
    ID_article: int

class Mod_Valider_Article(Mod):
    ID_article: int