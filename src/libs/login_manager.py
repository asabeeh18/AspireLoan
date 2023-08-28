from fastapi import HTTPException
from starlette import status

user_session = {}


def get_user_id_from_token(user_token):
    if user_token not in user_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User is not logged in or incorrect token",
        )
    return user_session[user_token]


def register_user_session(user_id):
    global user_session
    token = str(hash(str(user_id)))
    user_session[token] = user_id
    return token
