from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_access_token  # JWT 토큰 해독 함수
from app.db.session import get_db
from app.models.user import User

# OAuth2PasswordBearer는 로그인 엔드포인트의 URL(tokenUrl)을 필요로 함
# /auth/login을 사용
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    JWT 토큰을 검증하여 현재 로그인한 사용자(User)를 반환하는 의존성 함수입니다.
    - 토큰이 유효하지 않으면 401 Unauthorized 에러를 발생시킵니다.
    """
    payload = decode_access_token(token)  # JWT 토큰 해독
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    username: str = payload.get("sub")  # payload에 "sub" 항목에 사용자 이름을 담음
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # 데이터베이스에서 해당 username으로 사용자를 조회합니다.
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
