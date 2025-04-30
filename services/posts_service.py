from sqlalchemy import select, desc, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Posts, Users

from schemas.users import RegisterUser, UserProfile, UsersPosts
from schemas.posts import PostResponse


#GET
async def get_latest_posts(session:AsyncSession, page:int = 1):
    try:
        stmt = (
            select(Posts)
            .options(joinedload(Posts.user))
            .order_by(desc(Posts.post_id))
            .offset((page-1) * 10)
            .limit(10)
                )

        response = await session.execute(stmt)
        data = response.scalars().all()

        post_list = []

        for item in data:

            new_item = PostResponse(
                id=item.post_id,
                post_title=item.post_title,
                post_content=item.post_content,
                created_at=item.created_at.strftime("%d.%m.%y"),
                username=item.user.user_name
            )

            post_list.append(new_item)

        return post_list

    except Exception as e:
        return

async def get_post_by_id(
        post_id:int,
        session:AsyncSession
):
    try:
        stmt = select(Posts).where(Posts.post_id == post_id)
        response = await session.execute(stmt)
        data = response.scalar_one_or_none()
        return data
    except Exception as e:
        print(e)



# POST
async def create_post(title:str, content:str, user_id:int, session:AsyncSession):
    try:
        new_post = Posts(
            post_title = title,
            post_content = content,
            user_id = user_id
        )

        session.add(new_post)
        await session.commit()

        return True
    except Exception as e:
        return

#Delete
async def delete_post(
        post_id:int,
        session:AsyncSession
):
    try:
        stmt = delete(Posts).where(Posts.post_id == post_id)
        await session.execute(stmt)
        await session.commit()
        return True
    except Exception as e:
        print(e)





