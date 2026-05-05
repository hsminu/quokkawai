from pydantic import BaseModel


# 로그인한 사용자 정보
class UserResponse(BaseModel):
    userId: str
    provider: str
    providerUserId: str
    email: str | None = None
    nickname: str | None = None


# Google ID token 로그인 요청
class GoogleLoginRequest(BaseModel):
    idToken: str


# 로그인 성공 응답
class GoogleLoginResponse(BaseModel):
    success: bool = True
    user: UserResponse
