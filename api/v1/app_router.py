from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import get_current_user

from database.engine import get_async_session
from database.models import Users

from services.user_service import get_user_by_name_with_posts
from services.posts_service import get_latest_posts

from schemas.subscription import CheckSubscription

router = APIRouter(tags=["App"])

@router.get("/")
async def load_homepage(
        user:Users = Depends(get_current_user),
        session:AsyncSession = Depends(get_async_session)
):
    return {
        "msg" : "OK"
    }

@router.get("/posts")
async def load_posts(
        user:Users = Depends(get_current_user),
        session:AsyncSession = Depends(get_async_session)
):
    try:
        latest_posts = await get_latest_posts(session=session)
        return {
            "posts" : latest_posts
        }
    except Exception as e:
        print(e)

@router.get("/profile/{username}")
async def get_profile_info(username:str, session:AsyncSession = Depends(get_async_session)):

    data = await get_user_by_name_with_posts(name=username, session=session)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found."
        )

    return data


