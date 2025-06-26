from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    ename: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
