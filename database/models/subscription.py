from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from database.engine import Base

if TYPE_CHECKING:
    from database.models.users import Users

class Subscriptions(Base):
    __tablename__ = "subscriptions"

    sub_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    following_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    follower: Mapped["Users"] = relationship(
        "Users",
        foreign_keys=[follower_id],
        back_populates="following"
    )
    following: Mapped["Users"] = relationship(
        "Users",
        foreign_keys=[following_id],
        back_populates="followers"
    )
