from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str  # 회원가입 시 비밀번호를 입력받습니다.


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True  # ORM 객체를 자동으로 변환할 수 있도록 설정
