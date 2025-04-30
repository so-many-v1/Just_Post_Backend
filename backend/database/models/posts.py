from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import func, String, DateTime, ForeignKey

from database.engine import Base

from datetime import datetime

class Posts(Base):

    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_title:Mapped[str] = mapped_column(String(150), nullable=False)
    post_content:Mapped[str] = mapped_column(String(), nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(), default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())

    user_id:Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    user:Mapped["Users"] = relationship( "Users" , back_populates="posts")
