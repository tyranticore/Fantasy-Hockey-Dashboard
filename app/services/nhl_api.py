import httpx
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from app.config import NHL_API_BASE_URL

# Team tri-code mappings and details
NHL_TEAMS = {
    "ANA": "Anaheim Ducks", "BOS": "Boston Bruins", "BUF": "Buffalo Sabres",
    "CAR": "Carolina Hurricanes", "CBJ": "Columbus Blue Jackets", "CGY": "Calgary Flames",
    "CHI": "Chicago Blackhawks", "COL": "Colorado Avalanche", "DAL": "Dallas Stars",
    "DET": "Detroit Red Wings", "EDM": "Edmonton Oilers", "FLA": "Florida Panthers",
    "LAK": "Los Angeles Kings", "MIN": "Minnesota Wild", "MTL": "Montreal Canadiens",
    "NJD": "New Jersey Devils", "NSH": "Nashville Predators", "NYI": "New York Islanders",
    "NYR": "New York Rangers", "OTT": "Ottawa Senators", "PHI": "Philadelphia Flyers",
    "PIT": "Pittsburgh Penguins", "SJS": "San Jose Sharks", "SEA": "Seattle Kraken",
    "STL": "St. Louis Blues", "TBL": "Tampa Bay Lightning", "TOR": "Toronto Maple Leafs",
    "UTA": "Utah Hockey Club", "VAN": "Vancouver Canucks", "VGK": "Vegas Golden Knights",
    "WPG": "Winnipeg Jets", "WSH": "Washington Capitals"
}

# Cache structure to minimize requests
_schedule_cache = {"data": None, "timestamp": 0}
_team_schedule_cache = {"data": None, "timestamp": 0}

async def fetch_weekly_schedule() -> Dict[str, Any]:
    """
    Fetches the NHL weekly schedule and computes:
    - Number of games per team this week
    - Which games occur on 'off-nights' (days with <= 6 games, typically Mon/Wed/Fri/Sun)
    - Schedule matrix by day
    """
    now = datetime.now()
    url = f"{NHL_API_BASE_URL}/schedule/now"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                raw_data = resp.json()
                return process_schedule(raw_data)
    except Exception as e:
        print(f"Error fetching live NHL schedule: {e}")

    # Fallback simulated schedule if offline or API error
    return generate_fallback_schedule()

def process_schedule(data: Dict[str, Any]) -> Dict[str, Any]:
    game_week = data.get("gameWeek", [])
    
    # Days matrix
    days = []
    # Team stats: { 'EDM': { 'total_games': 4, 'off_night_games': 3, 'games': [...] } }
    team_breakdown: Dict[str, Dict[str, Any]] = {
        code: {
            "team_code": code,
            "team_name": name,
            "total_games": 0,
            "off_night_games": 0,
            "heavy_night_games": 0,
            "daily_opponent": {}
        }
        for code, name in NHL_TEAMS.items()
    }

    for day in game_week:
        date_str = day.get("date", "")
        day_of_week = day.get("dayAbbrev", "")
        games = day.get("games", [])
        game_count = len(games)

        # Off night rule: <= 6 games in the NHL on that day (or Mon, Wed, Fri, Sun)
        # Heavy nights are typically Tuesday, Thursday, Saturday where full lineups create bench locks
        is_off_night = game_count <= 6 or day_of_week in ["MON", "WED", "FRI", "SUN"]

        days.append({
            "date": date_str,
            "day": day_of_week,
            "game_count": game_count,
            "is_off_night": is_off_night
        })

        for game in games:
            away = game.get("awayTeam", {}).get("abbrev")
            home = game.get("homeTeam", {}).get("abbrev")

            if away in team_breakdown:
                team_breakdown[away]["total_games"] += 1
                if is_off_night:
                    team_breakdown[away]["off_night_games"] += 1
                else:
                    team_breakdown[away]["heavy_night_games"] += 1
                team_breakdown[away]["daily_opponent"][date_str] = f"@{home}"

            if home in team_breakdown:
                team_breakdown[home]["total_games"] += 1
                if is_off_night:
                    team_breakdown[home]["off_night_games"] += 1
                else:
                    team_breakdown[home]["heavy_night_games"] += 1
                team_breakdown[home]["daily_opponent"][date_str] = f"vs {away}"

    # Calculate a streaming quality score (0-100) based on off-night games and total games
    # Formula: (total_games * 15) + (off_night_games * 25)
    for team, stats in team_breakdown.items():
        score = (stats["total_games"] * 12) + (stats["off_night_games"] * 22)
        stats["streaming_score"] = min(100, score)

    return {
        "days": days,
        "teams": team_breakdown,
        "updated_at": datetime.utcnow().isoformat()
    }

def generate_fallback_schedule() -> Dict[str, Any]:
    """Generates realistic week schedule when running offline."""
    days = []
    base = datetime.now()
    days_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    
    for i, name in enumerate(days_names):
        d = base + timedelta(days=i)
        is_off = name in ["MON", "WED", "FRI", "SUN"]
        days.append({
            "date": d.strftime("%Y-%m-%d"),
            "day": name,
            "game_count": 4 if is_off else 11,
            "is_off_night": is_off
        })

    team_breakdown = {}
    import random
    random.seed(42)
    for code, full_name in NHL_TEAMS.items():
        total = random.choice([2, 3, 3, 4, 4, 4])
        off = random.randint(1, min(total, 3))
        team_breakdown[code] = {
            "team_code": code,
            "team_name": full_name,
            "total_games": total,
            "off_night_games": off,
            "heavy_night_games": total - off,
            "streaming_score": min(100, (total * 12) + (off * 22)),
            "daily_opponent": {}
        }

    return {
        "days": days,
        "teams": team_breakdown,
        "updated_at": datetime.utcnow().isoformat()
    }

async def fetch_player_landing(player_id: int) -> Optional[Dict[str, Any]]:
    """Fetches official NHL player details and recent game logs."""
    url = f"{NHL_API_BASE_URL}/player/{player_id}/landing"
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        pass
    return None
