import math
from typing import List, Dict, Any, Optional

def calculate_player_custom_rankings(
    players: List[Dict[str, Any]],
    league_categories: List[Dict[str, Any]],
    scoring_type: str = "head", # "head" (categories) or "head_point" (points)
    schedule_data: Optional[Dict[str, Any]] = None,
    category_weights: Optional[Dict[str, float]] = None
) -> List[Dict[str, Any]]:
    """
    Computes objective, mathematically-grounded player rankings based entirely
    on actual statistical production and league rules. ZERO reliance on Yahoo rankings.
    """
    if not players:
        return []

    if category_weights is None:
        category_weights = {}

    # Separate skaters and goalies for separate normalization
    skaters = [p for p in players if p.get("position") != "G"]
    goalies = [p for p in players if p.get("position") == "G"]

    ranked_skaters = _rank_player_group(skaters, league_categories, scoring_type, schedule_data, category_weights, is_goalie=False)
    ranked_goalies = _rank_player_group(goalies, league_categories, scoring_type, schedule_data, category_weights, is_goalie=True)

    all_ranked = ranked_skaters + ranked_goalies
    # Sort descending by custom calculated value score
    all_ranked.sort(key=lambda x: x.get("custom_value_score", 0), reverse=True)

    # Assign custom rank 1 to N
    for index, p in enumerate(all_ranked, start=1):
        p["custom_rank"] = index

    return all_ranked

def _rank_player_group(
    player_pool: List[Dict[str, Any]],
    league_categories: List[Dict[str, Any]],
    scoring_type: str,
    schedule_data: Optional[Dict[str, Any]],
    category_weights: Dict[str, float],
    is_goalie: bool
) -> List[Dict[str, Any]]:
    if not player_pool:
        return []

    # Filter categories matching this position type (P for skater, G for goalie)
    pos_type = "G" if is_goalie else "P"
    active_cats = [
        c for c in league_categories 
        if c.get("position_type") == pos_type or c.get("position_type") is None
    ]

    # If points league, rank by expected fantasy points & points per game
    if scoring_type in ["head_point", "point"]:
        return _rank_by_points(player_pool, active_cats, schedule_data)
    else:
        # H2H Categories / Roto: Rank by statistical Z-score sum
        return _rank_by_z_scores(player_pool, active_cats, schedule_data, category_weights)

def _rank_by_z_scores(
    player_pool: List[Dict[str, Any]],
    categories: List[Dict[str, Any]],
    schedule_data: Optional[Dict[str, Any]],
    category_weights: Dict[str, float]
) -> List[Dict[str, Any]]:
    # Step 1: Compute Mean and Standard Deviation for each active category
    stats_summary = {}
    for cat in categories:
        cat_key = cat.get("display_name") or cat.get("name")
        values = []
        for p in player_pool:
            val = p.get("stats", {}).get(cat_key, 0)
            if val is not None:
                try:
                    values.append(float(val))
                except (ValueError, TypeError):
                    values.append(0.0)
            else:
                values.append(0.0)

        n = len(values)
        if n > 1:
            mean = sum(values) / n
            variance = sum((x - mean) ** 2 for x in values) / (n - 1)
            std_dev = math.sqrt(variance) if variance > 0 else 1.0
        else:
            mean = values[0] if values else 0.0
            std_dev = 1.0

        stats_summary[cat_key] = {
            "mean": mean,
            "std_dev": std_dev if std_dev > 0.001 else 1.0,
            "is_negative": cat.get("is_negative", False),
            "weight": category_weights.get(cat_key, 1.0)
        }

    # Step 2: Compute Category Z-Scores for each player
    teams_schedule = schedule_data.get("teams", {}) if schedule_data else {}

    for p in player_pool:
        z_scores = {}
        total_z = 0.0
        player_stats = p.get("stats", {})

        for cat_key, summary in stats_summary.items():
            raw_val = player_stats.get(cat_key, 0)
            try:
                numeric_val = float(raw_val) if raw_val is not None else 0.0
            except (ValueError, TypeError):
                numeric_val = 0.0

            z = (numeric_val - summary["mean"]) / summary["std_dev"]
            if summary["is_negative"]:
                z = -z  # Invert negative stats like GAA or Losses

            weighted_z = z * summary["weight"]
            z_scores[cat_key] = round(z, 2)
            total_z += weighted_z

        # Step 3: Schedule Streaming Impact Calculation
        team_code = p.get("team_abbrev", "")
        team_sched = teams_schedule.get(team_code, {})
        weekly_games = team_sched.get("total_games", 3)
        off_night_games = team_sched.get("off_night_games", 1)
        
        # Streaming bonus: reward players who play 4 games or have high off-night density
        # Off-nights (Mon, Wed, Fri, Sun) ensure the player actually slots into an active roster spot
        streaming_score = round((weekly_games * 12.0) + (off_night_games * 22.0), 1)

        # Scale custom value score to intuitive 0 - 100 range
        # Baseline total_z typically ranges from -15 to +25 for skaters
        normalized_score = round(max(5.0, min(99.9, 50.0 + (total_z * 2.5))), 1)

        # Recent form boost: evaluate last 14 days / last 5 games trend if available
        form_trend = p.get("form_trend", "neutral") # hot, cold, neutral
        if form_trend == "hot":
            normalized_score = min(99.9, normalized_score + 3.5)
        elif form_trend == "cold":
            normalized_score = max(5.0, normalized_score - 2.5)

        p["custom_value_score"] = normalized_score
        p["category_z_scores"] = z_scores
        p["total_z_score"] = round(total_z, 2)
        p["weekly_games"] = weekly_games
        p["off_night_games"] = off_night_games
        p["streaming_score"] = streaming_score

    return player_pool

def _rank_by_points(
    player_pool: List[Dict[str, Any]],
    categories: List[Dict[str, Any]],
    schedule_data: Optional[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    teams_schedule = schedule_data.get("teams", {}) if schedule_data else {}

    for p in player_pool:
        total_pts = 0.0
        player_stats = p.get("stats", {})
        games_played = float(player_stats.get("GP", 1) or 1)
        if games_played <= 0:
            games_played = 1

        for cat in categories:
            cat_key = cat.get("display_name") or cat.get("name")
            multiplier = float(cat.get("point_value", 1.0))
            raw_val = player_stats.get(cat_key, 0)
            try:
                numeric_val = float(raw_val) if raw_val is not None else 0.0
            except (ValueError, TypeError):
                numeric_val = 0.0

            total_pts += (numeric_val * multiplier)

        fpts_per_game = total_pts / games_played
        
        team_code = p.get("team_abbrev", "")
        team_sched = teams_schedule.get(team_code, {})
        weekly_games = team_sched.get("total_games", 3)
        off_night_games = team_sched.get("off_night_games", 1)

        # Projected points this week
        projected_week_pts = round(fpts_per_game * weekly_games, 1)

        p["custom_value_score"] = round(total_pts, 1)
        p["fpts_per_game"] = round(fpts_per_game, 2)
        p["projected_week_pts"] = projected_week_pts
        p["weekly_games"] = weekly_games
        p["off_night_games"] = off_night_games
        p["streaming_score"] = round((weekly_games * 12.0) + (off_night_games * 22.0), 1)

    return player_pool
