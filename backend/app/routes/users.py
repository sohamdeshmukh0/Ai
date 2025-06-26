from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
# from fastapi_jwt.authlib import AuthlibJWTBackend
from passlib.context import CryptContext
from app.schemas import UserSignup, UserLogin
from app.models import find_user_by_email, create_user, update_user_password
from app.database import users_collection
from app.utils.email_utils import send_otp_email
import os
from datetime import datetime, timedelta
from random import randint

router = APIRouter(prefix="/auth", tags=["Auth"])

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Auth config
access_security = JwtAccessBearer(secret_key=os.getenv("JWT_SECRET_KEY", "your-secret-key"))



# access_security = JwtAccessBearer(
#     secret_key=os.getenv("JWT_SECRET_KEY", "your-secret-key"),
#     backend=AuthlibJWTBackend()
# )


@router.post("/signup")
async def signup(user: UserSignup):
    if await find_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    await create_user(user_dict)
    return JSONResponse(content={"msg": "User created"})

@router.post("/login")
async def login(user: UserLogin, response: Response):
    db_user = await find_user_by_email(user.email)

    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = access_security.create_access_token(subject={"email": user.email})
    access_security.set_access_cookie(response, access_token)

    return {"msg": "Login successful"}

@router.post("/logout")
async def logout(response: Response):
    access_security.unset_access_cookie(response)
    return {"msg": "Logged out successfully"}

@router.post("/forgot-password")
async def forgot_password(request: dict):
    email = request.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    user = await find_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = str(randint(100000, 999999))
    await users_collection.update_one(
        {"email": email},
        {"$set": {"otp": otp, "otp_created_at": datetime.utcnow()}}
    )
    try:
        send_otp_email(email, otp)
    except Exception:
        raise HTTPException(status_code=500, detail="Error sending OTP email")

    return {"msg": "OTP sent to email"}

@router.post("/change-password")
async def change_password(request: dict):
    email = request.get("email")
    otp = request.get("otp")
    new_password = request.get("new_password")

    user = await find_user_by_email(email)
    if not user or user.get("otp") != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP or email")

    otp_time = user.get("otp_created_at")
    if otp_time and datetime.utcnow() - otp_time > timedelta(minutes=10):
        raise HTTPException(status_code=400, detail="OTP expired")

    hashed_pw = pwd_context.hash(new_password)
    await update_user_password(email, hashed_pw)
    return {"msg": "Password updated successfully"}

@router.get("/protected")
async def protected(creds: JwtAuthorizationCredentials = Depends(access_security)):
    return {"msg": f"Hello, {creds.subject}!"}
