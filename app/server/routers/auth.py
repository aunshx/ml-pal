from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from auth.auth import generate_auth0_login_url, generate_auth0_logout_url
import requests
from urllib.parse import urlencode
from pydantic import BaseModel
import os

router = APIRouter()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

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
    token_response.raise_for_status()
    token = token_response.json().get("access_token")

    return TokenResponse(access_token=token, token_type="Bearer")

@router.get("/logout")
def logout():
    auth0_logout_url = generate_auth0_logout_url()
    return RedirectResponse(url=auth0_logout_url)
