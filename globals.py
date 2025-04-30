from dotenv import load_dotenv
from models import User
from dataclasses import dataclass
import os

load_dotenv()

# BATTLE_NET_CLIENT_ID = os.getenv("BATTLE_NET_CLIENT_ID")
# BATTLE_NET_SECRET_KEY = os.getenv("BATTLE_NET_SECRET_KEY")
# BATTLE_NET_REGION = os.getenv("BATTLE_NET_REGION")
# BATTLE_NET_REDIRECT_URI = os.getenv("BATTLE_NET_REDIRECT_URI")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_OPENID_URL = "https://steamcommunity.com/openid"
STEAM_RETURN_URL = "http://localhost:8000/auth/steam/callback"
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")


@dataclass
class SteamAccountSummary:
    username: str or None
    profile_url: str or None
    avatar_url: str or None
