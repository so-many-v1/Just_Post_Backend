import time

from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import get_current_user

from database.engine import get_async_session
from database.models import Users

from services.posts_service import create_post, get_post_by_id, delete_post

from schemas.posts import CreatePost
from schemas.kafka import CreatePostEvent

from kafka import PostProducer

router = APIRouter()
PRODUCER = PostProducer()

@router.post("/write-post", tags=["Posts"])
async def create_user_post(
        data:CreatePost,
        user: Users = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    isCreated = await create_post(
        title=data.title,
        content=data.content,
        user_id=user.user_id,
        session=session
    )

    if isCreated:

        event = CreatePostEvent(
            event_id=PRODUCER.generate_event_id(),
            time=time.time(),
            writer_username=user.user_name
        )

        await PRODUCER.send_event(payload=event)

        return {
            "msg": "Post Created",
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating post"
        )


@router.delete("/delete-post/{post_id}")
async def delete_user_post(
        post_id:int,
        user:Users = Depends(get_current_user),
        session:AsyncSession = Depends(get_async_session)
):
    try:
        current_post = await get_post_by_id(post_id=post_id, session=session)


        if current_post.user_id != user.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not allowed."
            )

        isDeleted = await delete_post(post_id=post_id, session=session)

        if isDeleted:
            return {
                "msg" : "Post deleted."
            }

    except Exception as e:
        print(e)
