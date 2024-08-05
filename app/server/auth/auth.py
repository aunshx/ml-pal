import os
from urllib.parse import urlencode
from dotenv import load_dotenv

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
