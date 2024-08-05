
# Dumbledore - Server

Model selection service server for mlpl.ai

## Prerequisites

- Python 3.8+
- PostgreSQL
- Git

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/aunshx/archx-ai.git

cd app/server
```

### 2. Set up the virtual environment

```bash
python3 -m venv venv
```

Windows:

```bash
.\venv\Scripts\activate
```

macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up .env file in the server folder

```bash
DATABASE_URL=postgresql://super:!%40QW12qwaszx@postgresql-180434-0.cloudclusters.net:10056/mp_dumbledore
AUTH0_DOMAIN=dev-mw81v5ryzhqlgb73.us.auth0.com
API_AUDIENCE=https://dev-mw81v5ryzhqlgb73.us.auth0.com/api/v2/
CLIENT_ID=C76sDcksezix8w6m2cSfI9iTwVgriewy
CLIENT_SECRET=RtsNkW-Q_IZRfwjaQoxwTzNAPAY1MjjgiOwVdpWboYaMfPnrHCOKrDozZkxRM9Ek
REDIRECT_URI=http://localhost:8000/callback
LOGOUT_REDIRECT_URI=http://localhost:8000
```

### 4. Start the server

```bash
uvicorn main:app --reload
```
