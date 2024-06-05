import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JSWT_ALGORITHM = config("algorithm")

# Function return the generated token
def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(userID: str, fullName: str, role: str, email: str):
    payload = {
        "user_id": userID,
        "fullname": fullName,
        "role": role,
        "email": email,
        "expires": time.time() + 86400
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JSWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JSWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
