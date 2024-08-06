from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
from fastapi.security import OAuth2PasswordBearer
from urllib.parse import urlencode
from auth.auth import generate_auth0_login_url, generate_auth0_logout_url
import os

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserInfo(BaseModel):
    user_id: str
    email: str
    name: str

@router.get("/login")
def login():
    auth0_login_url = generate_auth0_login_url()
    return RedirectResponse(url=auth0_login_url)

@router.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not found")

    token_url = f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "authorization_code",
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "code": code,
        "redirect_uri": os.getenv("REDIRECT_URI"),
    }

    token_response = requests.post(token_url, headers=headers, data=urlencode(body))
    if token_response.status_code != 200:
        raise HTTPException(status_code=token_response.status_code, detail="Error retrieving access token")
    token = token_response.json().get("access_token")

    frontend_redirect_url = f"http://localhost:3000/auth/callback?access_token={token}"
    return RedirectResponse(frontend_redirect_url)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/get-user")
def get_user(token: str = Depends(oauth2_scheme)):
    user_info_url = f"https://{os.getenv('AUTH0_DOMAIN')}/userinfo"
    user_info_response = requests.get(user_info_url, headers={"Authorization": f"Bearer {token}"})
    if user_info_response.status_code != 200:
        raise HTTPException(status_code=user_info_response.status_code, detail="Error retrieving user info")

    user_info = user_info_response.json()
    return {
        "user_id": user_info["sub"],
        "email": user_info["email"],
        "name": user_info["name"],
    }

@router.get("/logout")
def logout():
    auth0_logout_url = generate_auth0_logout_url()
    return RedirectResponse(url=auth0_logout_url)
