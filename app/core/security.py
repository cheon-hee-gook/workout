from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from .config import settings

# 비밀번호 해싱을 위한 컨텍스트 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    주어진 평문 비밀번호와 해시된 비밀번호를 비교합니다.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    주어진 비밀번호를 해싱하여 반환합니다.
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    주어진 데이터를 기반으로 JWT 토큰을 생성합니다.
    """
    to_encode = data.copy()
    # 토큰 만료 시간 설정
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    # 토큰 생성: settings.JWT_SECRET_KEY와 HS256 알고리즘 사용
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    JWT 토큰을 해독하여 데이터를 반환합니다.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        return None
