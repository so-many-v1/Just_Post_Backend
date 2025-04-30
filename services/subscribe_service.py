from sqlalchemy import select, desc, delete, func, exists
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from database.models import Users, Posts, Subscriptions

from services.user_service import get_user_by_name

from helpers import generate_verification_email_link


#GET
async def check_subscription(
        follower:str,
        follow_to:str,
        session:AsyncSession
):
    follower_user = await get_user_by_name(name=follower, session=session)
    following_user = await get_user_by_name(name=follow_to, session=session)

    if not follower_user or not following_user:
        return False

    stmt = select(
        exists().where(
            Subscriptions.follower_id == follower_user.user_id,
            Subscriptions.following_id == following_user.user_id
        )
    )

    result = await session.execute(stmt)
    (is_subscribed,) = result.one()

    return is_subscribed

#Delete
async def delete_subscription(sub_id:int, session:AsyncSession):

    stmt = delete(Subscriptions).where(Subscriptions.sub_id == sub_id)
    await session.execute(stmt)
    await session.commit()