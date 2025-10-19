# stage0 Task
RESTful API endpoint that returns your profile information along with a dynamic cat fact fetched from an external API.

# built with Python(Django + DRF)

## Setup
1. Clone repo
2. Create & activate virtualenv:
   python -m venv .venv
   source .venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
4. Create `.env` from `.env.example`:
   USER_EMAIL=danieleinstien@gmail.com
   USER_NAME=Daniel Eze
   USER_STACK=Python/Django
   CATFACT_API_URL=https://catfact.ninja/fact
   CATFACT_TIMEOUT=3

## Run locally
python manage.py migrate
python manage.py runserver 8000

GET http://127.0.0.1:8000/me
    https://web-production-8806c.up.railway.app/me


