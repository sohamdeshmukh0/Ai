from .database import users_collection, questions_collection
from datetime import datetime

async def find_user_by_email(email: str):
    return await users_collection.find_one({"email": email})

async def create_user(user_data: dict):
    return await users_collection.insert_one(user_data)

async def update_user_password(email: str, hashed_password: str):
    await users_collection.update_one(
        {"email": email},
        {"$set": {"password": hashed_password}, "$unset": {"otp": "", "otp_created_at": ""}}
    )

async def store_prompt_and_response_in_db(context: str, questions: list):
    await questions_collection.insert_one({
        "context": context,
        "questions": questions,
        "created_at": datetime.utcnow()
    })    
