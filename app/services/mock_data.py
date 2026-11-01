from typing import List, Dict, Any

MOCK_CATEGORIES = [
    {"stat_id": "1", "display_name": "G", "name": "Goals", "position_type": "P", "is_negative": False, "point_value": 6.0},
    {"stat_id": "2", "display_name": "A", "name": "Assists", "position_type": "P", "is_negative": False, "point_value": 4.0},
    {"stat_id": "3", "display_name": "+/-", "name": "Plus/Minus", "position_type": "P", "is_negative": False, "point_value": 1.0},
    {"stat_id": "4", "display_name": "PIM", "name": "Penalty Minutes", "position_type": "P", "is_negative": False, "point_value": 0.5},
    {"stat_id": "5", "display_name": "PPP", "name": "Powerplay Points", "position_type": "P", "is_negative": False, "point_value": 2.0},
    {"stat_id": "6", "display_name": "SHP", "name": "Shorthanded Points", "position_type": "P", "is_negative": False, "point_value": 3.0},
    {"stat_id": "7", "display_name": "SOG", "name": "Shots on Goal", "position_type": "P", "is_negative": False, "point_value": 0.9},
    {"stat_id": "8", "display_name": "HIT", "name": "Hits", "position_type": "P", "is_negative": False, "point_value": 0.5},
    {"stat_id": "9", "display_name": "BLK", "name": "Blocks", "position_type": "P", "is_negative": False, "point_value": 1.0},
    {"stat_id": "10", "display_name": "W", "name": "Wins", "position_type": "G", "is_negative": False, "point_value": 5.0},
    {"stat_id": "11", "display_name": "GAA", "name": "Goals Against Average", "position_type": "G", "is_negative": True, "point_value": -3.0},
    {"stat_id": "12", "display_name": "SV%", "name": "Save Percentage", "position_type": "G", "is_negative": False, "point_value": 5.0},
    {"stat_id": "13", "display_name": "SHO", "name": "Shutouts", "position_type": "G", "is_negative": False, "point_value": 5.0}
]

MOCK_USER_ROSTER: List[Dict[str, Any]] = [
    {
        "id": "101",
        "name": "Connor McDavid",
        "team_abbrev": "EDM",
        "position": "C",
        "eligible_positions": ["C"],
        "status": "Healthy",
        "form_trend": "hot",
        "pp_unit": "PP1",
        "stats": {"GP": 15, "G": 9, "A": 17, "+/-": 6, "PIM": 8, "PPP": 10, "SHP": 1, "SOG": 54, "HIT": 12, "BLK": 6}
    },
    {
        "id": "102",
        "name": "Nathan MacKinnon",
        "team_abbrev": "COL",
        "position": "C",
        "eligible_positions": ["C"],
        "status": "Healthy",
        "form_trend": "hot",
        "pp_unit": "PP1",
        "stats": {"GP": 16, "G": 8, "A": 21, "+/-": 8, "PIM": 12, "PPP": 9, "SHP": 0, "SOG": 68, "HIT": 14, "BLK": 8}
    },
    {
        "id": "103",
        "name": "Artemi Panarin",
        "team_abbrev": "NYR",
        "position": "LW",
        "eligible_positions": ["LW"],
        "status": "Healthy",
        "form_trend": "hot",
        "pp_unit": "PP1",
        "stats": {"GP": 15, "G": 10, "A": 12, "+/-": 4, "PIM": 4, "PPP": 7, "SHP": 0, "SOG": 52, "HIT": 7, "BLK": 9}
    },
    {
        "id": "104",
        "name": "William Nylander",
        "team_abbrev": "TOR",
        "position": "RW",
        "eligible_positions": ["RW"],
        "status": "Healthy",
        "form_trend": "neutral",
        "pp_unit": "PP1",
        "stats": {"GP": 16, "G": 11, "A": 9, "+/-": 2, "PIM": 6, "PPP": 6, "SHP": 0, "SOG": 60, "HIT": 5, "BLK": 7}
    },
    {
        "id": "105",
        "name": "Cale Makar",
        "team_abbrev": "COL",
        "position": "D",
        "eligible_positions": ["D"],
        "status": "Healthy",
        "form_trend": "hot",
        "pp_unit": "PP1",
        "stats": {"GP": 16, "G": 6, "A": 19, "+/-": 9, "PIM": 4, "PPP": 11, "SHP": 0, "SOG": 48, "HIT": 15, "BLK": 24}
    },
    {
        "id": "106",
        "name": "Rasmus Dahlin",
        "team_abbrev": "BUF",
        "position": "D",
        "eligible_positions": ["D"],
        "status": "Healthy",
        "form_trend": "neutral",
        "pp_unit": "PP1",
        "stats": {"GP": 15, "G": 4, "A": 9, "+/-": -2, "PIM": 16, "PPP": 4, "SHP": 0, "SOG": 42, "HIT": 34, "BLK": 28}
    },
    {
        "id": "107",
        "name": "Tom Wilson",
        "team_abbrev": "WSH",
        "position": "RW",
        "eligible_positions": ["RW"],
        "status": "Healthy",
        "form_trend": "neutral",
        "pp_unit": "PP2",
        "stats": {"GP": 15, "G": 6, "A": 6, "+/-": 5, "PIM": 26, "PPP": 3, "SHP": 1, "SOG": 35, "HIT": 48, "BLK": 14}
    },
    {
        "id": "108",
        "name": "Connor Hellebuyck",
        "team_abbrev": "WPG",
        "position": "G",
        "eligible_positions": ["G"],
        "status": "Healthy",
        "form_trend": "hot",
        "pp_unit": "-",
        "stats": {"GP": 12, "W": 11, "GAA": 1.85, "SV%": 0.934, "SHO": 3}
    },
    {
        "id": "109",
        "name": "Jeremy Swayman",
        "team_abbrev": "BOS",
        "position": "G",
        "eligible_positions": ["G"],
        "status": "Healthy",
        "form_trend": "cold",
        "pp_unit": "-",
        "stats": {"GP": 11, "W": 5, "GAA": 3.14, "SV%": 0.896, "SHO": 1}
    }
]

MOCK_WAIVER_POOL: List[Dict[str, Any]] = [
    {
        "id": "201",
        "name": "Wyatt Johnston",
        "team_abbrev": "DAL",
        "position": "C",
        "eligible_positions": ["C", "RW"],
        "status": "Free Agent",
        "ownership_pct": 68,
        "form_trend": "hot",
        "pp_unit": "PP1",
        "notes": "Surged to top line with Stankoven and Benn; playing 19:20 TOI",
        "stats": {"GP": 15, "G": 7, "A": 9, "+/-": 7, "PIM": 4, "PPP": 5, "SHP": 1, "SOG": 46, "HIT": 20, "BLK": 14}
    },
    {
        "id": "202",
        "name": "Gabriel Vilardi",
        "team_abbrev": "WPG",
        "position": "RW",
        "eligible_positions": ["C", "RW"],
        "status": "Free Agent",
        "ownership_pct": 59,
        "form_trend": "hot",
        "pp_unit": "PP1",
        "notes": "Locked on lethal WPG PP1 with Scheifele and Connor; 5-game point streak",
        "stats": {"GP": 16, "G": 8, "A": 7, "+/-": 9, "PIM": 6, "PPP": 6, "SHP": 0, "SOG": 39, "HIT": 16, "BLK": 11}
    },
    {
        "id": "203",
        "name": "Logan Stankoven",
        "team_abbrev": "DAL",
        "position": "RW",
        "eligible_positions": ["RW"],
        "status": "Free Agent",
        "ownership_pct": 52,
        "form_trend": "hot",
        "pp_unit": "PP2",
        "notes": "Calder contender, leading all rookies in primary assists and high-danger chances",
        "stats": {"GP": 15, "G": 4, "A": 12, "+/-": 6, "PIM": 2, "PPP": 4, "SHP": 0, "SOG": 41, "HIT": 11, "BLK": 8}
    },
    {
        "id": "204",
        "name": "JJ Peterka",
        "team_abbrev": "BUF",
        "position": "LW",
        "eligible_positions": ["LW", "RW"],
        "status": "Free Agent",
        "ownership_pct": 55,
        "form_trend": "hot",
        "pp_unit": "PP1",
        "notes": "Shooting at heavy volume (3.5 SOG/game) on Buffalo's dynamic top unit",
        "stats": {"GP": 14, "G": 7, "A": 6, "+/-": 1, "PIM": 4, "PPP": 4, "SHP": 0, "SOG": 49, "HIT": 9, "BLK": 5}
    },
    {
        "id": "205",
        "name": "Dylan Guenther",
        "team_abbrev": "UTA",
        "position": "RW",
        "eligible_positions": ["LW", "RW"],
        "status": "Free Agent",
        "ownership_pct": 64,
        "form_trend": "neutral",
        "pp_unit": "PP1",
        "notes": "Utah's primary powerplay trigger man with a booming one-timer",
        "stats": {"GP": 15, "G": 8, "A": 5, "+/-": -1, "PIM": 8, "PPP": 5, "SHP": 0, "SOG": 44, "HIT": 18, "BLK": 10}
    },
    {
        "id": "206",
        "name": "Connor Zary",
        "team_abbrev": "CGY",
        "position": "C",
        "eligible_positions": ["C", "LW"],
        "status": "Free Agent",
        "ownership_pct": 24,
        "form_trend": "neutral",
        "pp_unit": "PP1",
        "notes": "Calgary off-night streamer gem; plays 4 games this week (3 off-nights)",
        "stats": {"GP": 15, "G": 4, "A": 6, "+/-": 3, "PIM": 6, "PPP": 2, "SHP": 0, "SOG": 33, "HIT": 17, "BLK": 12}
    },
    {
        "id": "207",
        "name": "Radko Gudas",
        "team_abbrev": "ANA",
        "position": "D",
        "eligible_positions": ["D"],
        "status": "Free Agent",
        "ownership_pct": 47,
        "form_trend": "neutral",
        "pp_unit": "-",
        "notes": "Elite peripheral monster: #1 in Hits and Blocks among available D-men",
        "stats": {"GP": 14, "G": 1, "A": 2, "+/-": -3, "PIM": 32, "PPP": 0, "SHP": 0, "SOG": 22, "HIT": 58, "BLK": 36}
    },
    {
        "id": "208",
        "name": "Anthony Stolarz",
        "team_abbrev": "TOR",
        "position": "G",
        "eligible_positions": ["G"],
        "status": "Free Agent",
        "ownership_pct": 62,
        "form_trend": "hot",
        "pp_unit": "-",
        "notes": "Stealing starter's net in Toronto; elite sub-2.20 GAA and .925+ SV%",
        "stats": {"GP": 10, "W": 7, "GAA": 2.18, "SV%": 0.927, "SHO": 1}
    },
    {
        "id": "209",
        "name": "Pyotr Kochetkov",
        "team_abbrev": "CAR",
        "position": "G",
        "eligible_positions": ["G"],
        "status": "Free Agent",
        "ownership_pct": 74,
        "form_trend": "hot",
        "pp_unit": "-",
        "notes": "Primary starter behind Carolina's stifling league-leading shot suppression defense",
        "stats": {"GP": 11, "W": 9, "GAA": 2.35, "SV%": 0.910, "SHO": 1}
    },
    {
        "id": "210",
        "name": "Jake Walman",
        "team_abbrev": "SJS",
        "position": "D",
        "eligible_positions": ["D"],
        "status": "Free Agent",
        "ownership_pct": 39,
        "form_trend": "hot",
        "pp_unit": "PP1",
        "notes": "Quarterbacking top PP unit, logging 24+ mins TOI with heavy blocks and shots",
        "stats": {"GP": 14, "G": 2, "A": 8, "+/-": -4, "PIM": 10, "PPP": 4, "SHP": 0, "SOG": 34, "HIT": 22, "BLK": 38}
    }
]

MOCK_MATCHUP = {
    "week": 6,
    "user_team": {
        "name": "The Great Eight",
        "manager": "Ty",
        "rank": 2,
        "record": "4-1-0"
    },
    "opponent_team": {
        "name": "Puck Dynasty",
        "manager": "Dave",
        "rank": 3,
        "record": "3-2-0"
    },
    "category_scores": [
        {"cat": "G", "user": 18, "opp": 15, "status": "winning"},
        {"cat": "A", "user": 29, "opp": 22, "status": "winning"},
        {"cat": "+/-", "user": 4, "opp": 9, "status": "losing"},
        {"cat": "PIM", "user": 18, "opp": 32, "status": "losing"},
        {"cat": "PPP", "user": 12, "opp": 8, "status": "winning"},
        {"cat": "SHP", "user": 1, "opp": 0, "status": "winning"},
        {"cat": "SOG", "user": 142, "opp": 156, "status": "losing"},
        {"cat": "HIT", "user": 62, "opp": 94, "status": "losing"},
        {"cat": "BLK", "user": 51, "opp": 48, "status": "winning"},
        {"cat": "W", "user": 3, "opp": 2, "status": "winning"},
        {"cat": "GAA", "user": 2.24, "opp": 2.89, "status": "winning"},
        {"cat": "SV%", "user": 0.923, "opp": 0.904, "status": "winning"},
        {"cat": "SHO", "user": 1, "opp": 0, "status": "winning"}
    ],
    "overall_score": "8-5-0",
    "trailing_categories": ["SOG", "HIT", "PIM", "+/-"]
}
