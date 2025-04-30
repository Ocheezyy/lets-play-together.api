from fastapi import APIRouter
from openid.consumer.consumer import Consumer, SUCCESS
from openid.store.memstore import MemoryStore
from fastapi.responses import RedirectResponse
from fastapi import Request, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import User
from auth import create_steam_jwt
from globals import STEAM_OPENID_URL, STEAM_RETURN_URL

auth_router = APIRouter()


# class UserCreate(BaseModel):
#     email: str
#     password: str
#
#
# class UserLogin(BaseModel):
#     email: str
#     password: str


@auth_router.get("/steam")
async def login_with_steam(request: Request):
    consumer = Consumer({}, MemoryStore())
    auth_request = consumer.begin(STEAM_OPENID_URL)
    redirect_url = auth_request.redirectURL(
        realm="http://localhost:8000/",  # your backend
        return_to=STEAM_RETURN_URL
    )
    return {"url": redirect_url}


@auth_router.get("/steam/callback")
async def steam_callback(request: Request, session: AsyncSession = Depends(get_session)):
    consumer = Consumer({}, MemoryStore())
    query = dict(request.query_params)
    openid_response = consumer.complete(query, request.url._url)

    if openid_response.status == SUCCESS:
        claimed_id = openid_response.getDisplayIdentifier()
        steam_id = claimed_id.split("/")[-1]

        stmt = select(User).where(User.steam_id == steam_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            user = User(steam_id=steam_id)
            session.add(user)
            await session.commit()

        # Ideally: Generate a token (e.g., short-lived JWT or session key)
        # For now, redirect with steam_id in query
        token = create_steam_jwt({"steam_id": steam_id})
        redirect_url = f"http://localhost:5173/login-success?token={token}"
        return RedirectResponse(redirect_url)

    return RedirectResponse("http://localhost:5173/login-failed")


# @auth_router.post("/unlink/{provider}")
# async def unlink_account(
#     provider: str,
#     current_user: User = Depends(get_current_user),
#     session: AsyncSession = Depends(get_session),
# ):
#     if provider == "steam":
#         current_user.steam_id = None
#         current_user.steam_persona = None
#         current_user.steam_avatar = None
#         current_user.steam_profile_url = None
#     # elif provider == "battlenet":
#     #     current_user.battlenet_id = None
#     #     current_user.battlenet_tag = None
#     else:
#         raise HTTPException(400, "Unsupported provider")
#
#     session.add(current_user)
#     await session.commit()
#     return {"message": f"{provider} account unlinked."}
#
#
# @auth_router.post("/register")
# async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
#     stmt = select(User).where(User.email == user.email)
#     result = await session.execute(stmt)
#     existing = result.scalar().first()
#     if existing:
#         raise HTTPException(400, "User already exists")
#     db_user = User(email=user.email, hashed_password=hash_password(user.password))
#     session.add(db_user)
#     await session.commit()
#     await session.refresh(db_user)
#     return {"id": db_user.id, "email": db_user.email}
#
#
# @auth_router.post("/token")
# async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
#     stmt = select(User).where(User.email == user.email)
#     result = await session.execute(stmt)
#     db_user = result.scalar().first()
#     if not db_user or not verify_password(user.password, db_user.hashed_password):
#         raise HTTPException(401, "Invalid credentials")
#     token = create_access_token({"sub": str(db_user.id)})
#     return {"access_token": token, "token_type": "bearer"}
