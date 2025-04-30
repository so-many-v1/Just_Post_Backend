from sqlalchemy import select, desc, delete, func, exists
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from database.models import Users, Posts, Subscriptions

from schemas.users import RegisterUser, UserProfile, UsersPosts

from helpers import generate_verification_email_link


# Get
async def get_user_by_name_with_posts(
        name: str,
        session: AsyncSession
):
    user_stmt = (select(Users)
            .options(joinedload(Users.posts))
            .where(Users.user_name == name))



    response = await session.execute(user_stmt)
    user = response.unique().scalar_one_or_none()

    follower_stmt = select(func.count(Subscriptions.sub_id)).where(Subscriptions.following_id == user.user_id)
    following_stmt = select(func.count(Subscriptions.sub_id)).where(Subscriptions.follower_id == user.user_id)

    follower_amount = (await session.execute(follower_stmt)).scalar()
    following_amount = (await session.execute(following_stmt)).scalar()

    users_posts = []

    for post in sorted(user.posts, key=lambda x: x.post_id, reverse=True):
        item = UsersPosts(
            id=post.post_id,
            post_title=post.post_title,
            post_content=post.post_content,
            created_at=post.created_at.strftime("%d.%m.%y"),
        )

        users_posts.append(item)

    json = UserProfile(
        name=user.user_name,
        posts=users_posts,
        followers_amount=follower_amount,
        following_amount=following_amount
    )

    return json


async def get_user_by_name(
        name: str,
        session: AsyncSession
):
    stmt = select(Users).where(Users.user_name == name)
    response = await session.execute(stmt)
    data = response.scalar_one_or_none()
    return data


async def get_user_by_verification_link(
        link: str,
        session: AsyncSession
):
    stmt = select(Users).where(Users.verify_email_link == link)
    response = await session.execute(stmt)
    data = response.scalar_one_or_none()
    return data

# Post
async def create_user(
        name,
        email,
        hashed_password,
        session: AsyncSession
):
    try:
        user = Users(
            user_name=name,
            password=hashed_password,
            email=email,
            verify_email_link=generate_verification_email_link()
        )

        session.add(user)
        await session.commit()
    except Exception as e:
        print(e)


#Update
async def mark_user_verified(
        user:Users,
        session: AsyncSession
):
    user.verify_email_link = None
    user.verify_email_sent_at = None
    user.is_verified = True

    await session.commit()


#Delete
async def delete_user(
        verification_link: str,
        session: AsyncSession
):
    stmt = delete(Users).where(Users.verify_email_link == verification_link)
    await session.execute(stmt)
    await session.commit()


