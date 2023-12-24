from fastapi import APIRouter, status
from validators.Auth import *
from controllers.Authentification import Authentification
from utils.HTTPResponse import HTTPResponse

router = APIRouter()

@router.post("/login")
def handle_login(account : Account_To_LogIn ):
    Authentification.log_in(account.email, account.password)

@router.post("/signup")
def handle_signup(account : Account_To_SignUp ):
    Authentification.sign_up(account.email, account.password, account.nom)

@router.get("/myAccount")
def handle_signup(account : Account ):
    Authentification.get_profile(account.token)

@router.post("/updateAccount")
def handle_signup(account : Account_To_Update ):
    Authentification.edit_profile(account.token, account.nom, account.email, account.password)
