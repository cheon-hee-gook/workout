from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.core.config import settings

router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    로그인 API
    - OAuth2PasswordRequestForm은 username과 password 필드를 포함합니다.
    - 입력받은 username을 기준으로 사용자를 조회하고, 비밀번호를 검증합니다.
    - 검증에 성공하면 JWT 토큰을 생성하여 반환합니다.
    """
    # 사용자 조회
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # 비밀번호 검증
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # 토큰 만료 시간 설정 (설정 파일의 JWT_EXPIRE_MINUTES 사용)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # JWT 토큰 생성 (payload에 "sub": username 포함)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
