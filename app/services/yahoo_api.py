import json
import time
import httpx
from typing import Dict, List, Any, Optional
from urllib.parse import urlencode
from app.config import (
    YAHOO_CLIENT_ID,
    YAHOO_CLIENT_SECRET,
    YAHOO_REDIRECT_URI,
    YAHOO_API_BASE_URL,
    YAHOO_OAUTH_TOKEN_URL,
    YAHOO_OAUTH_AUTH_URL
)

def get_authorization_url(client_id: str, redirect_uri: str, state: str = "state_123") -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "state": state,
        "language": "en-us"
    }
    return f"{YAHOO_OAUTH_AUTH_URL}?{urlencode(params)}"

async def exchange_code_for_tokens(code: str, client_id: str, client_secret: str, redirect_uri: str) -> Optional[Dict[str, Any]]:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code,
        "grant_type": "authorization_code"
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(YAHOO_OAUTH_TOKEN_URL, data=data, headers=headers)
        if resp.status_code == 200:
            token_data = resp.json()
            # Calculate absolute expiry timestamp
            expires_in = token_data.get("expires_in", 3600)
            token_data["expires_at"] = time.time() + expires_in - 60
            return token_data
        else:
            print(f"Yahoo OAuth Token Error ({resp.status_code}): {resp.text}")
            return None

async def refresh_access_token(refresh_token: str, client_id: str, client_secret: str) -> Optional[Dict[str, Any]]:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "oob",
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(YAHOO_OAUTH_TOKEN_URL, data=data, headers=headers)
        if resp.status_code == 200:
            token_data = resp.json()
            expires_in = token_data.get("expires_in", 3600)
            token_data["expires_at"] = time.time() + expires_in - 60
            return token_data
        else:
            print(f"Yahoo OAuth Refresh Error ({resp.status_code}): {resp.text}")
            return None

async def yahoo_api_request(url: str, access_token: str) -> Optional[Dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            raise PermissionError("Access token expired")
        else:
            print(f"Yahoo API request failed ({resp.status_code}): {resp.text}")
            return None

async def get_user_leagues(access_token: str) -> List[Dict[str, Any]]:
    """Fetches user's current NHL fantasy leagues."""
    url = f"{YAHOO_API_BASE_URL}/users;use_login=1/games;game_keys=nhl/leagues?format=json"
    data = await yahoo_api_request(url, access_token)
    leagues = []
    if not data:
        return leagues
    
    try:
        users = data.get("fantasy_content", {}).get("users", {})
        user_obj = users.get("0", {}).get("user", [])
        games = user_obj[1].get("games", {})
        game_obj = games.get("0", {}).get("game", [])
        league_items = game_obj[1].get("leagues", {})
        
        for k, item in league_items.items():
            if k == "count":
                continue
            league_data = item.get("league", [{}])[0]
            leagues.append({
                "league_key": league_data.get("league_key"),
                "name": league_data.get("name"),
                "num_teams": league_data.get("num_teams"),
                "season": league_data.get("season"),
                "scoring_type": league_data.get("scoring_type"),
                "current_week": league_data.get("current_week")
            })
    except Exception as e:
        print(f"Error parsing Yahoo leagues: {e}")
    return leagues

async def get_league_settings(access_token: str, league_key: str) -> Dict[str, Any]:
    """Fetches scoring categories and settings for the given league."""
    url = f"{YAHOO_API_BASE_URL}/league/{league_key}/settings?format=json"
    data = await yahoo_api_request(url, access_token)
    if not data:
        return {}
    
    try:
        league_content = data.get("fantasy_content", {}).get("league", [{}, {}])
        meta = league_content[0]
        settings = league_content[1].get("settings", [{}])[0]
        
        stat_categories_raw = settings.get("stat_categories", {}).get("stats", [])
        stat_modifiers_raw = settings.get("stat_modifiers", {}).get("stats", [])
        
        # Build modifiers map if points league
        modifiers_map = {}
        for mod in stat_modifiers_raw:
            stat_info = mod.get("stat", {})
            modifiers_map[str(stat_info.get("stat_id"))] = float(stat_info.get("value", 1.0))
            
        parsed_categories = []
        for cat in stat_categories_raw:
            stat = cat.get("stat", {})
            stat_id = str(stat.get("stat_id"))
            parsed_categories.append({
                "stat_id": stat_id,
                "name": stat.get("name"),
                "display_name": stat.get("display_name"),
                "position_type": stat.get("position_type"), # P (Player/Skater) or G (Goalie)
                "is_negative": bool(stat.get("is_negative_stat", False) or stat.get("display_name") in ["GA", "L"]),
                "point_value": modifiers_map.get(stat_id, 1.0)
            })
            
        return {
            "league_key": meta.get("league_key"),
            "name": meta.get("name"),
            "scoring_type": settings.get("scoring_type", "head"), # head (categories), head_point (points)
            "categories": parsed_categories,
            "roster_positions": settings.get("roster_positions", [])
        }
    except Exception as e:
        print(f"Error parsing Yahoo league settings: {e}")
        return {}
