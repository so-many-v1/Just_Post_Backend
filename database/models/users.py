import time
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func, String, DateTime, ForeignKey, Boolean

from database.engine import Base

if TYPE_CHECKING:
    from database.models import Posts, Subscriptions

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    verify_email_link: Mapped[str] = mapped_column(String(255), nullable=True)
    verify_email_sent_at: Mapped[str] = mapped_column(String(50), default=lambda: str(time.time()), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())

    posts: Mapped[List["Posts"]] = relationship("Posts", back_populates="user")
    followers: Mapped[List["Subscriptions"]] = relationship(
        "Subscriptions",
        foreign_keys="Subscriptions.following_id",
        back_populates="following"
    )
    following: Mapped[List["Subscriptions"]] = relationship(
        "Subscriptions",
        foreign_keys="Subscriptions.follower_id",
        back_populates="follower"
    )
