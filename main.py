from fastapi import FastAPI, Depends
from auth import decode_access_token, get_current_user
from db import get_session
from models import User
from sqlmodel import Session
from routers import auth, steam

app = FastAPI()

app.include_router(auth.auth_router, prefix="/auth", tags=["auth"])
app.include_router(steam.steam_router, prefix="/steam", tags=["steam"])


@app.get("/me")
def me(payload=Depends(decode_access_token), session: Session = Depends(get_session)):
    user_id = int(payload["sub"])
    user = session.get(User, user_id)
    return user


@app.get("/me/accounts")
def get_linked_accounts(current_user: User = Depends(get_current_user)):
    return {
        "steam": {
            "id": current_user.steam_id,
            "persona": current_user.steam_persona,
            "avatar": current_user.steam_avatar,
        },
    }



