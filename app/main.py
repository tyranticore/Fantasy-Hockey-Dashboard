import json
from pathlib import Path
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import (
    BASE_DIR,
    ADMIN_PASSWORD,
    YAHOO_CLIENT_ID,
    YAHOO_CLIENT_SECRET,
    YAHOO_REDIRECT_URI,
    DEV_MOCK_DATA
)
from app.database import (
    init_db,
    get_db,
    get_setting,
    set_setting,
    OAuthToken,
    LeagueSettingsCache
)
from app.auth import (
    create_access_token,
    get_current_user_optional,
    COOKIE_NAME,
    verify_password,
    hash_password
)
from app.services.nhl_api import fetch_weekly_schedule
from app.services.yahoo_api import (
    get_authorization_url,
    exchange_code_for_tokens,
    get_user_leagues,
    get_league_settings
)
from app.services.ranking_engine import calculate_player_custom_rankings
from app.services.mock_data import (
    MOCK_CATEGORIES,
    MOCK_USER_ROSTER,
    MOCK_WAIVER_POOL,
    MOCK_MATCHUP
)

app = FastAPI(title="PuckMetrics - Fantasy Hockey Analytics Hub")

# Mount static files and templates
static_path = Path(__file__).parent / "static"
static_path.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

@app.on_event("startup")
def startup():
    init_db()

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
async def login_submit(
    request: Request,
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    saved_pwd = get_setting(db, "admin_password", ADMIN_PASSWORD)
    
    # Check if matches plain or hashed
    is_valid = (password == saved_pwd) or (hash_password(password) == saved_pwd)
    
    if not is_valid:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid master password. Please try again."},
            status_code=400
        )

    # Issue session cookie
    token = create_access_token({"sub": "admin"})
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=86400 * 30,
        samesite="lax"
    )
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(COOKIE_NAME)
    return response

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user_optional(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    # Fetch live NHL weekly schedule
    schedule = await fetch_weekly_schedule()

    # Get settings from DB or defaults
    yahoo_client_id = get_setting(db, "yahoo_client_id", YAHOO_CLIENT_ID)
    yahoo_client_secret = get_setting(db, "yahoo_client_secret", YAHOO_CLIENT_SECRET)
    yahoo_redirect_uri = get_setting(db, "yahoo_redirect_uri", YAHOO_REDIRECT_URI)

    # Check OAuth token status
    oauth_token = db.query(OAuthToken).filter(OAuthToken.provider == "yahoo").first()
    has_yahoo_auth = oauth_token is not None

    # Load categories & scoring type
    scoring_type = get_setting(db, "scoring_type", "head")
    categories = MOCK_CATEGORIES

    # Rank player pools using custom mathematical ranking engine (Zero Yahoo ranks!)
    ranked_roster = calculate_player_custom_rankings(
        players=list(MOCK_USER_ROSTER),
        league_categories=categories,
        scoring_type=scoring_type,
        schedule_data=schedule
    )

    ranked_waivers = calculate_player_custom_rankings(
        players=list(MOCK_WAIVER_POOL),
        league_categories=categories,
        scoring_type=scoring_type,
        schedule_data=schedule
    )

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "matchup": MOCK_MATCHUP,
        "roster": ranked_roster,
        "waivers": ranked_waivers,
        "roster_json": json.dumps(ranked_roster),
        "waivers_json": json.dumps(ranked_waivers),
        "schedule": schedule,
        "has_yahoo_auth": has_yahoo_auth,
        "yahoo_client_id": yahoo_client_id,
        "yahoo_client_secret": yahoo_client_secret,
        "yahoo_redirect_uri": yahoo_redirect_uri,
        "scoring_type": scoring_type
    })

# ================= Yahoo OAuth Routes =================

@app.get("/auth/yahoo/login")
async def yahoo_login(db: Session = Depends(get_db)):
    client_id = get_setting(db, "yahoo_client_id", YAHOO_CLIENT_ID)
    redirect_uri = get_setting(db, "yahoo_redirect_uri", YAHOO_REDIRECT_URI)
    if not client_id:
        return HTMLResponse("<p>Error: Yahoo Client ID is missing. Please configure it in Settings first.</p>", status_code=400)
    
    auth_url = get_authorization_url(client_id, redirect_uri)
    return RedirectResponse(auth_url)

@app.get("/auth/yahoo/callback")
async def yahoo_callback(request: Request, code: str = None, state: str = None, db: Session = Depends(get_db)):
    if not code:
        return HTMLResponse("<p>OAuth error: No authorization code received from Yahoo.</p>", status_code=400)

    client_id = get_setting(db, "yahoo_client_id", YAHOO_CLIENT_ID)
    client_secret = get_setting(db, "yahoo_client_secret", YAHOO_CLIENT_SECRET)
    redirect_uri = get_setting(db, "yahoo_redirect_uri", YAHOO_REDIRECT_URI)

    tokens = await exchange_code_for_tokens(code, client_id, client_secret, redirect_uri)
    if not tokens or "access_token" not in tokens:
        return HTMLResponse("<p>Failed to exchange code for Yahoo tokens. Please check your client credentials and redirect URI.</p>", status_code=400)

    # Save to database
    token_row = db.query(OAuthToken).filter(OAuthToken.provider == "yahoo").first()
    if not token_row:
        token_row = OAuthToken(
            provider="yahoo",
            access_token=tokens["access_token"],
            refresh_token=tokens.get("refresh_token", ""),
            expires_at=tokens.get("expires_at", 0)
        )
        db.add(token_row)
    else:
        token_row.access_token = tokens["access_token"]
        if "refresh_token" in tokens:
            token_row.refresh_token = tokens["refresh_token"]
        token_row.expires_at = tokens.get("expires_at", 0)
    db.commit()

    return RedirectResponse(url="/?yahoo_connected=1", status_code=status.HTTP_302_FOUND)

@app.post("/api/settings/yahoo")
async def save_yahoo_settings(
    client_id: str = Form(...),
    client_secret: str = Form(...),
    redirect_uri: str = Form(...),
    db: Session = Depends(get_db)
):
    set_setting(db, "yahoo_client_id", client_id.strip())
    set_setting(db, "yahoo_client_secret", client_secret.strip())
    set_setting(db, "yahoo_redirect_uri", redirect_uri.strip())
    return RedirectResponse(url="/#settings", status_code=status.HTTP_302_FOUND)

@app.get("/api/schedule")
async def get_schedule_api():
    sched = await fetch_weekly_schedule()
    return JSONResponse(content=sched)
