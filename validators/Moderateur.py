from pydantic import BaseModel

class Mod(BaseModel):
    token: str

class Mod_Rectifier_Article(Mod):
    ID_article: int
    titre: str = None
    texte: str = None
    resume: str = None
    date_publication: str = None

class Mod_Supprimer_Article(Mod):
    ID_article: int

class Mod_Valider_Article(Mod):
    ID_article: int