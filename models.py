from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

    steam_id: Optional[str] = Field(default=None, index=True, unique=True)
    steam_persona: Optional[str] = None
    steam_avatar: Optional[str] = None
    steam_profile_url: Optional[str] = None

    # battlenet_id: Optional[str] = Field(default=None, index=True, unique=True)
    # battlenet_tag: Optional[str] = None
