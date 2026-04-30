from pydantic import BaseModel

#############################
#구글 로그인 사용자 정보 타입
############################



# 구글 로그인 기반 사용자 정보
class User(BaseModel):
    # 앱 내부에서 사용하는 사용자 ID
    userId: str

    # 구글 계정 고유 ID, 중복 가입 식별
    googleUserId: str

    email: str | None = None
    name: str | None = None
    profileImageUrl: str | None = None
    

    createdAt: str
    updatedAt: str
    lastLoginAt: str


# 프론트에서 구글 로그인 성공 후 백엔드로 보내는 요청
class GoogleLoginRequest(BaseModel):
    idToken: str


# 구글 로그인 성공 응답
class GoogleLoginResponse(BaseModel):
    success: bool = True

    # 우리 앱에서 발급하는 access token
    accessToken: str
    user: User


# 내 정보 조회 응답
class UserResponse(BaseModel):
    success: bool = True
    user: User
