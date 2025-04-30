from fastapi import FastAPI, Depends
from auth import get_current_user  # decode_access_token, get_current_user
from db import get_session
from models import User
from sqlmodel import Session
from routers import auth, steam
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",  # Vite/React default dev server
    # Add more origins here if needed (e.g., deployed frontend URL)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # or ["*"] for all
    allow_credentials=True,
    allow_methods=["*"],                # or specify ['GET', 'POST'] etc.
    allow_headers=["*"],
)


app.include_router(auth.auth_router, prefix="/auth", tags=["auth"])
app.include_router(steam.steam_router, prefix="/steam", tags=["steam"])


# @app.get("/me/accounts")
# def get_linked_accounts(current_user: User = Depends(get_current_user)):
#     return {
#         "steam": {
#             "id": current_user.steam_id,
#             "persona": current_user.steam_persona,
#             "avatar": current_user.steam_avatar,
#         },
#     }



