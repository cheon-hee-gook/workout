from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from datetime import datetime
from app.db.base import Base


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # ForeignKey를 통해 users 테이블의 id와 연관 (어떤 사용자가 기록했는지)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    sets = Column(Integer, nullable=False)   # 운동 세트 수
    reps = Column(Integer, nullable=False)   # 반복 횟수
    weight = Column(Float, nullable=True)      # 중량 (없을 수도 있으므로 nullable)
    date = Column(DateTime, default=datetime.utcnow)  # 기록 일자 (기본값: 현재 시간)
    note = Column(String, nullable=True)       # 추가 메모 (선택적)
