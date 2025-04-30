from fastapi import APIRouter
from auth import get_current_user
from fastapi import Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from db import get_session
from models import User
from httpx import AsyncClient
from globals import STEAM_API_KEY
from helpers import get_steam_accounts_summaries


steam_router = APIRouter()


@steam_router.get("/me")
def me(user: User = Depends(get_current_user)):
    return user


@steam_router.get("/friends")
async def get_steam_friends(current_user: User = Depends(get_current_user)):
    steam_id = current_user.steam_id
    url = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/"
    params = {"key": STEAM_API_KEY, "steamid": steam_id, "relationship": "friend"}

    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    if "friendslist" not in data:
        raise HTTPException(403, "Friends list may be private.")

    friends_steam_ids = [x["steamid"] for x in data["friendslist"]["friends"]]
    friends_data = await get_steam_accounts_summaries(friends_steam_ids)

    return friends_data


@steam_router.get("/games")
async def get_steam_games(current_user: User = Depends(get_current_user),):
    async with AsyncClient() as client:
        response = await client.get(
            f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={current_user.steam_id}&include_appinfo=true&include_played_free_games=true"
        )
        return response.json()
