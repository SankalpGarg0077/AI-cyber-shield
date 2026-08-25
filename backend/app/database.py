import os
import firebase_admin
from firebase_admin import credentials, firestore

from app.config import settings

def init_firebase():
    if not firebase_admin._apps:
        # Check direct path in backend folder
        cred_path = settings.FIREBASE_CREDENTIALS_PATH
        if not os.path.isabs(cred_path):
            # Look inside backend directory directly
            cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), cred_path)
            cred_path = os.path.abspath(cred_path)

        # Fallback check if file is in current backend folder
        if not os.path.exists(cred_path):
            backend_dir = os.path.dirname(os.path.dirname(__file__))
            fallback_path = os.path.join(backend_dir, "serviceAccountKey.json")
            if os.path.exists(fallback_path):
                cred_path = fallback_path

        if not os.path.exists(cred_path):
            raise FileNotFoundError(
                f"Firebase credentials not found at '{cred_path}'"
            )
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

init_firebase()

# Export Firestore database instance
db = firestore.client()