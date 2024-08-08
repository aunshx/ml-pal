import os
from urllib.parse import urlencode
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
import requests

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
LOGOUT_REDIRECT_URI = os.getenv("LOGOUT_REDIRECT_URI")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ALGORITHMS = ["RS256"]

def generate_auth0_login_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "audience": API_AUDIENCE,
    }
    print('HELLO generate')
    return f"https://{AUTH0_DOMAIN}/authorize?" + urlencode(params)

def generate_auth0_logout_url():
    params = {
        "client_id": CLIENT_ID,
        "returnTo": LOGOUT_REDIRECT_URI,
    }
    return f"https://{AUTH0_DOMAIN}/v2/logout?" + urlencode(params)


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"https://{AUTH0_DOMAIN}/authorize",
    tokenUrl=f"https://{AUTH0_DOMAIN}/oauth/token"
)

def get_public_key():
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    return response.json()['keys'][0]

def verify_token(token: str = Depends(oauth2_scheme)):
    public_key = get_public_key()
    try:
        payload = jwt.decode(token, public_key, algorithms=ALGORITHMS, audience=API_AUDIENCE)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

