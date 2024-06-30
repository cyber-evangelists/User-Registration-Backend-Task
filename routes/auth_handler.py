import time
from typing import Dict

import jwt  # Responsible for encoding and decoding generated token strings

# It is better to use .env file rather than explicitly using the secret and algorithm in the code file directly. Sample_env given in base dir
# from decouple import config


# JWT_SECRET = config("secret")
# JWT_ALGORITHM = config("algorithm")


JWT_SECRET = "Author_Saad_Abdur_Razzaq"
JWT_ALGORITHM = "HS256"


def token_response(token: str) -> Dict[str, str]:
    """
    Helper function for returning generated tokens
    """

    return {
        "access_token": token
    }


def sign_jwt(cnic: str) -> Dict[str, str]:
    """
    Function to generate a JWT token
    """

    payload = {
        "cnic": cnic,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    """
    Function to decode a JWT token
    """

    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time(
        ) else None
    except BaseException:
        return {}
