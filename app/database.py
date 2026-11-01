import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SystemSetting(Base):
    __tablename__ = "system_settings"
    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OAuthToken(Base):
    __tablename__ = "oauth_tokens"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String(50), default="yahoo", unique=True)
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)
    token_type = Column(String(20), default="bearer")
    expires_at = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LeagueSettingsCache(Base):
    __tablename__ = "league_settings_cache"
    league_key = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    scoring_type = Column(String(50), default="head") # head, head_point, roto
    stat_categories_json = Column(Text, nullable=False) # JSON array of stat categories & weights
    active_season = Column(String(20), default="20242025")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_setting(db, key: str, default: str = "") -> str:
    item = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    return item.value if item and item.value is not None else default

def set_setting(db, key: str, value: str):
    item = db.query(SystemSetting).filter(SystemSetting.key == key).first()
    if not item:
        item = SystemSetting(key=key, value=value)
        db.add(item)
    else:
        item.value = value
    db.commit()
