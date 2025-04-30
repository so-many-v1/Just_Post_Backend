from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from auth.utils import get_current_user

from database.engine import get_async_session
from database.models import Users, Subscriptions

from services.subscribe_service import check_subscription, delete_subscription
from services.user_service import get_user_by_name

from schemas.subscription import CheckSubscription, SubscribeToSchema

router = APIRouter(tags=["Subscription"])


#GET
@router.post("/profile/{follower_username}/subscription-status")
async def get_profile_info(
        follower_username:str,
        user_to_follow:CheckSubscription,
        session:AsyncSession = Depends(get_async_session)
):
    is_subscribed = await check_subscription(follower=follower_username,
                                             follow_to=user_to_follow.following_to_username,
                                             session=session)

    if is_subscribed:
        return {
            "subscribed" : True
        }
    else:
        return {
            "subscribed": False
        }

#POST
@router.post("/profile/{username}/subscribe")
async def create_subscription(
        follow_to_username: SubscribeToSchema,
        user:Users = Depends(get_current_user),
        session:AsyncSession = Depends(get_async_session)
):

    follow_to_user = await get_user_by_name(
        name=follow_to_username.following_to_username,
        session=session
    )

    if not follow_to_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {follow_to_username.following_to_username} follow not found."
        )

    stmt = select(Subscriptions).where(
        Subscriptions.follower_id == user.user_id,
        Subscriptions.following_id == follow_to_user.user_id
    )

    exists_subscription = await session.execute(stmt)
    if exists_subscription.scalar():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already subscribed."
        )
    new_subscription = Subscriptions(
        follower_id=user.user_id,
        following_id=follow_to_user.user_id
    )

    session.add(new_subscription)
    await session.commit()

    return {
        "msg" : "subscribed"
    }

#Delete
@router.delete("/profile/{username}/unsubscribe")
async def create_subscription(
        follow_to_username: SubscribeToSchema,
        user:Users = Depends(get_current_user),
        session:AsyncSession = Depends(get_async_session)
):

    follow_to_user = await get_user_by_name(
        name=follow_to_username.following_to_username,
        session=session
    )

    if not follow_to_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {follow_to_username.following_to_username} follow not found."
        )

    stmt = select(Subscriptions).where(
        Subscriptions.follower_id == user.user_id,
        Subscriptions.following_id == follow_to_user.user_id
    )

    data = await session.execute(stmt)
    subscription = data.scalar_one_or_none()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Subscribtion not exist"
        )

    await delete_subscription(sub_id=subscription.sub_id, session=session)

    return {
        "msg" : "unsubscribed"
    }

