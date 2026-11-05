import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-1234567890")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

# Yahoo Fantasy OAuth
YAHOO_CLIENT_ID = os.getenv("YAHOO_CLIENT_ID", "")
YAHOO_CLIENT_SECRET = os.getenv("YAHOO_CLIENT_SECRET", "")
YAHOO_REDIRECT_URI = os.getenv("YAHOO_REDIRECT_URI", "http://localhost:8585/auth/yahoo/callback")

# Database
DB_PATH = DATA_DIR / "fantasy_hockey.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Dev / Mock Mode (set to "true" or "1" to enable rich demo data)
DEV_MOCK_DATA = os.getenv("DEV_MOCK_DATA", "true").lower() in ("true", "1", "yes")

# NHL API Base
NHL_API_BASE_URL = "https://api-web.nhle.com/v1"
YAHOO_API_BASE_URL = "https://fantasysports.yahooapis.com/fantasy/v2"
YAHOO_OAUTH_TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"
YAHOO_OAUTH_AUTH_URL = "https://api.login.yahoo.com/oauth2/request_auth"
