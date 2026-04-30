from pydantic import BaseModel


class User(BaseModel):
    userId: str
    googleUserId: str
    email: str | None = None
    name: str | None = None
    profileImageUrl: str | None = None
    createdAt: str
    updatedAt: str
    lastLoginAt: str


class GoogleLoginRequest(BaseModel):
    idToken: str


class GoogleLoginResponse(BaseModel):
    success: bool = True
    accessToken: str
    user: User


class UserResponse(BaseModel):
    success: bool = True
    user: User
