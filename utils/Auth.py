import jwt
from models.Utilisateur import Utilisateur
from models.Moderateur import Moderateur
from models.Administrateur import Administrateur
from utils.Creds import JwtCreds
from utils.Date import Date
from utils.Role import Role

class Token_Payload():
    id : int
    nom : str
    role : Role
    expiration : Date

    def __init__(self, id, nom, role) -> None:
        self.id = id
        self.nom = nom
        self.role = role
        self.expiration = Date.today().date_after_days(30)

    def __init__(self, token_payload : dict) -> None:
        self.id = token_payload.get("id")
        self.nom = token_payload.get("nom")
        self.role = Role(token_payload.get("role"))
        self.expiration = Date(token_payload.get("expiration"))

    def get_Token_Payload(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "role": self.role.value,
            "expiration": self.expiration.get_date()
        }
    def get_role(self) -> Role:
        return self.role
    def get_id(self) -> int:
        return self.id
    def get_expiration(self) -> Date:
        return self.expiration

def jwt_encode(payload : Token_Payload):
    payload = payload.get_Token_Payload()
    encoded_jwt = jwt.encode(payload=payload, key=JwtCreds["Secret"], algorithm="HS256")
    return encoded_jwt
def jwt_decode(token : str):
    decoded_jwt = jwt.decode(jwt=token, key=JwtCreds["Secret"], algorithm="HS256")
    token_payload = Token_Payload(decoded_jwt)
    return token_payload

def generate_token(Account : Utilisateur | Moderateur | Administrateur):
    def generate_token_Utilisateur(User: Utilisateur):
        payload = Token_Payload(User.ID_Utilisateur, User.Email, Role.USER)
        return jwt_encode(payload.get_Token_Payload())
    def generate_token_Moderateur(Mod: Moderateur):
        payload = Token_Payload(Mod.ID_Moderateur, Mod.Email, Role.MOD)        
        return jwt_encode(payload.get_Token_Payload())
    def generate_token_Administrateur(Admin: Administrateur):
        payload = Token_Payload(Admin.ID_Administrateur, Admin.Email, Role.ADMIN)
        return jwt_encode(payload.get_Token_Payload())
    if (isinstance(Account, Utilisateur) ):
        return generate_token_Utilisateur(Account)
    elif (isinstance(Account, Moderateur) ):
        return generate_token_Moderateur(Account)
    elif (isinstance(Account, Administrateur) ):
        return generate_token_Administrateur(Account)
    else:
        return None
    
def check_token(token: str) -> bool | Token_Payload:
    payload = jwt_decode(str)
    expiration = payload.get_expiration()
    if (expiration.is_before_today() ):
        return False
    else:
        return payload