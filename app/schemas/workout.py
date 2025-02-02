from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class WorkoutBase(BaseModel):
    user_id: int
    category_id: int
    sets: int
    reps: int
    weight: Optional[float] = None   # 중량은 선택적
    note: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    """운동 기록 생성 시 사용되는 스키마 (추가 로직이 없으므로 WorkoutBase와 동일)"""
    pass


class WorkoutResponse(WorkoutBase):
    id: int          # DB에서 자동 생성된 id
    date: datetime   # 기록 생성일시

    class Config:
        orm_mode = True  # ORM 객체(SQLAlchemy)와 호환되도록 설정
