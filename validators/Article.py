from pydantic import BaseModel

class Get_Article(BaseModel):
    ID_Utilisateur : int
    
class Add_Delete_Article(Get_Article):
    ID_Article : int