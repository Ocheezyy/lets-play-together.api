from fastapi import APIRouter
from auth import get_current_user
from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models import User
from httpx import AsyncClient
from globals import STEAM_API_KEY


steam_router = APIRouter()


@steam_router.get("/steam/friends")
async def get_steam_friends(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if not current_user.steam_id:
        raise HTTPException(400, "Steam account not linked.")

    steam_id = current_user.steam_id
    url = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/"
    params = {"key": STEAM_API_KEY, "steamid": steam_id, "relationship": "friend"}

    async with AsyncClient() as client:
        response = await client.get(url, params=params)
        data = response.json()

    if "friendslist" not in data:
        raise HTTPException(403, "Friends list may be private.")

    return data["friendslist"]["friends"]


@steam_router.get("/steam_games/{steam_id}")
async def route_get_steam_games(steam_id: int):
    async with AsyncClient() as client:
        response = await client.get(
            f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id}&include_appinfo=true&include_played_free_games=true"
        )
        return response.json()