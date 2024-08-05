from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
import requests
import os
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
LOGOUT_REDIRECT_URI = os.getenv("LOGOUT_REDIRECT_URI")
ALGORITHMS = ["RS256"]

class TokenData(BaseModel):
    sub: str = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_jwks():
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    response.raise_for_status()
    return response.json()

def get_rsa_key(token):
    unverified_header = jwt.get_unverified_header(token)
    jwks = get_jwks()
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if not rsa_key:
        raise HTTPException(status_code=401, detail="Unable to find appropriate key")
    return rsa_key

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        rsa_key = get_rsa_key(token)
        payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer=f'https://{AUTH0_DOMAIN}/')
        token_data = TokenData(sub=payload.get("sub"))
        return token_data
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def generate_auth0_login_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "audience": API_AUDIENCE,
    }
    return f"https://{AUTH0_DOMAIN}/authorize?" + urlencode(params)

def generate_auth0_logout_url():
    params = {
        "client_id": CLIENT_ID,
        "returnTo": LOGOUT_REDIRECT_URI,
    }
    return f"https://{AUTH0_DOMAIN}/v2/logout?" + urlencode(params)
