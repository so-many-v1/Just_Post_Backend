import time
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_async_session
from kafka.auth.LoginProducer import LoginProducer

from schemas.users import RegisterUser, LoginUser
from schemas.kafka import LoginEventSchema, RegistrationEventSchema, DeleteEventSchema

from services.user_service import create_user, get_user_by_name, get_user_by_verification_link,delete_user, mark_user_verified

from kafka import RegisterProducer,LoginProducer,DeleteProducer

from auth import utils

router = APIRouter(prefix="/login", tags=["Auth"])

login_producer = LoginProducer()
register_producer = RegisterProducer()
delete_producer = DeleteProducer()

#GET
@router.get("/verify-email")
async def verify_user(
        token:str,
        session:AsyncSession = Depends(get_async_session)
):
    try:
        print(token)
        user = await get_user_by_verification_link(link=token, session=session)

        link = user.verify_email_link
        link_iat = float(user.verify_email_sent_at)
        current_time = time.time()

        auth_time_delta = current_time - link_iat

        print(auth_time_delta)

        if auth_time_delta > 2 * 3600:

            event = DeleteEventSchema(
                event_id=delete_producer.generate_event_id(),
                time=time.time(),
                username=user.user_name,
                email=user.email
            )

            await delete_producer.send_event(payload=event)
            await delete_user(verification_link=link,session=session)
            return {"msg": "Verification link expired. User deleted."}

        await mark_user_verified(user=user,session=session)
        return RedirectResponse(url="http://localhost:5173/login", status_code=303)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server Error.")


@router.post("/sign-up")
async def register_user(data:RegisterUser, session:AsyncSession = Depends(get_async_session)):
    existing_user = await get_user_by_name(name=data.name, session=session)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Username already exists!"
        )

    if data.password != data.confirmed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    encoded_password = utils.password_to_hashed(password=data.password)
    await create_user(name=data.name, hashed_password=encoded_password, email=data.email, session=session)

    event = RegistrationEventSchema(
        event_id=register_producer.generate_event_id(),
        time=time.time(),
        username=data.name,
        email=data.email
    )

    print("start send event")
    await register_producer.send_event(payload=event)
    print("end send event")

@router.post("/sing-in")
async def login_user(data:LoginUser, session:AsyncSession = Depends(get_async_session)):
    user = await get_user_by_name(name=data.name, session=session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect login or password"
        )

    is_valid_pass = utils.validate_password(hashed_password=user.password, password=data.password)
    is_verified = user.is_verified

    if not is_valid_pass:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect login or password"
        )

    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please check and verify your email"
        )

    current_time = datetime.now(timezone.utc)

    jwt_payload = {
        "sub": str(user.user_id),
        "name": data.name,
        "email": user.email,
        "iat": int(current_time.timestamp()),
        "exp": int((current_time + timedelta(hours=1)).timestamp())
    }

    token = utils.encode_jwt(payload=jwt_payload)

    event = RegistrationEventSchema(
        event_id=login_producer.generate_event_id(),
        time=time.time(),
        username=data.name,
        email=user.email
    )

    await login_producer.send_event(payload=event)

    return {
        "msg": "OK",
        "token": token,
    }




