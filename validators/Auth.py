from pydantic import BaseModel
from typing import Optional

class Account(BaseModel):
    token : str

class Account_To_LogIn(BaseModel):
    email : str
    password : str

class Account_To_SignUp(Account_To_LogIn):
    nom : str

class Account_To_Update(Account):
    nom : Optional[str]
    email : Optional[str] 
    password : Optional[str]