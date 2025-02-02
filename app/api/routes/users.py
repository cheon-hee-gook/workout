from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User
from app.db.session import get_db
from app.core.security import get_password_hash
from app.services.user_service import create_user, get_user_by_username

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    회원가입 API
    - 사용자로부터 username, email, password를 받아 새 사용자를 생성합니다.
    """
    # 사용자 존재 여부 체크
    existing_user = get_user_by_username(db, username=user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    # 비밀번호 해싱
    hashed_password = get_password_hash(user.password)
    # 사용자 생성 (서비스 레이어를 통해 실제 DB 저장)
    new_user = create_user(db, username=user.username, email=user.email, hashed_password=hashed_password)
    return new_user
