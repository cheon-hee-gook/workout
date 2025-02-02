from sqlalchemy.orm import Session
from app.models.user import User


def get_user_by_username(db: Session, username: str):
    """
    주어진 username으로 사용자 정보를 DB에서 조회합니다.
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, username: str, email: str, hashed_password: str):
    """
    새 사용자를 생성하여 DB에 저장합니다.
    """
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)   # 새 사용자 추가
    db.commit()        # 변경사항 커밋
    db.refresh(new_user)  # DB에서 최신 정보 가져오기
    return new_user
