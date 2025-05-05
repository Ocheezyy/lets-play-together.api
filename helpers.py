from httpx import AsyncClient
from globals import SteamAccountSummary, STEAM_API_KEY

summary_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"


def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


async def get_steam_accounts_summaries(steam_ids: list[str]) -> list[dict]:
    summaries = []

    async with AsyncClient() as client:
        for chunk in chunked(steam_ids, 100):
            params = {"key": STEAM_API_KEY, "steamids": ",".join(chunk)}
            response = await client.get(summary_url, params=params)
            data = response.json()

            players = data.get("response", {}).get("players", [])
            for player in players:
                try:
                    # Extract Steam profile details
                    steam_id = player["steamid"]
                    steam_username = player.get("personaname")
                    steam_profile_url = player.get("profileurl")
                    steam_avatar = player.get("avatarfull")
                    summaries.append({
                        "steam_id": steam_id,
                        "steam_username": steam_username,
                        "steam_profile_url": steam_profile_url,
                        "steam_avatar": steam_avatar
                    })
                except Exception as e:
                    print("Failed to extract summary for player: {}, error: {}".format(player, e))

    # sorted_summaries = sorted(
    #     summaries,
    #     key=lambda summary: summary["steam_username"].lower() if summary["steam_username"] else ""
    # )
    return summaries


async def get_steam_account_summary(steam_id: str) -> SteamAccountSummary:
    params = {"key": STEAM_API_KEY, "steamids": steam_id}

    async with AsyncClient() as client:
        response = await client.get(summary_url, params=params)
        data = response.json()

    if "response" in data and "players" in data["response"]:
        player = data["response"]["players"][0]  # We only expect one player object
        # print(player)

        # Extract Steam profile details
        steam_username = player.get("personaname")
        steam_profile_url = player.get("profileurl")
        steam_avatar = player.get("avatarfull")

        return SteamAccountSummary(username=steam_username, profile_url=steam_profile_url, avatar_url=steam_avatar)

    else:
        return SteamAccountSummary(None, None, None)


async def get_friends_steam_games(steam_ids: list[str]) -> dict[str, list[dict]]:
    result_obj: dict[str, list] = {}
    async with AsyncClient() as client:
        for steam_id in steam_ids:
            response = await client.get(
                f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={steam_id}&include_appinfo=true&include_played_free_games=true"
            )
            data = response.json()

            if "response" in data and "games" in data["response"]:
                game_count: int = data["response"]["game_count"]
                games = data["response"]["games"]
                result_obj[steam_id] = games
                # print(json.dumps(games, indent=2, ensure_ascii=True))

    return result_obj
