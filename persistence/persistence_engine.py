import os
import firebase_admin
from firebase_admin import credentials, db
from asgiref.sync import sync_to_async

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = "https://gestion-grandeurs-ec791-default-rtdb.europe-west1.firebasedatabase.app"

if not firebase_admin._apps:
    cred = credentials.Certificate(os.path.join(BASE_DIR, "certificat_firebase.json"))
    firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})


@sync_to_async
def persist_mesure_firebase(data: dict):
    db.reference("mesures", url=DATABASE_URL).push(data)
    print(f"[Firebase] saved ✔ {data}")