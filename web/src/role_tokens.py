import datetime
import jwt
from typing import Dict, Optional
from .config import config

SECRET_KEY = config.get('jwt_secret_key', 'change-me')


def create_token(user_id: str, role: str, expires_in: int = 3600) -> str:
    """Create a signed JWT for a user with the given role."""
    payload = {
        'sub': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def verify_token(token: str) -> Optional[Dict]:
    """Return the decoded token if valid, else None."""
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return data
    except Exception:
        return None

