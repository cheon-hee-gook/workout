from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.workout import Workout

router = APIRouter()


@router.get("/weekly")
def get_weekly_statistics(user_id: int, db: Session = Depends(get_db)):
    """
    주간 통계 API
    - 최근 7일간 사용자의 운동 기록을 날짜별로 그룹화하여,
      운동 횟수, 평균 중량, 평균 반복 횟수를 계산합니다.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)

    stats = (
        db.query(
            func.date(Workout.date).label("date"),
            func.count(Workout.id).label("workout_count"),
            func.avg(Workout.weight).label("avg_weight"),
            func.avg(Workout.reps).label("avg_reps")
        )
        .filter(
            Workout.user_id == user_id,
            Workout.date >= start_date,
            Workout.date <= end_date
        )
        .group_by(func.date(Workout.date))
        .all()
    )
    return stats


@router.get("/monthly")
def get_monthly_statistics(user_id: int, db: Session = Depends(get_db)):
    """
    월간 통계 API
    - 최근 30일간 사용자의 운동 기록을 날짜별로 그룹화하여,
      운동 횟수, 평균 중량, 평균 반복 횟수를 계산합니다.
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)

    stats = (
        db.query(
            func.date(Workout.date).label("date"),
            func.count(Workout.id).label("workout_count"),
            func.avg(Workout.weight).label("avg_weight"),
            func.avg(Workout.reps).label("avg_reps")
        )
        .filter(
            Workout.user_id == user_id,
            Workout.date >= start_date,
            Workout.date <= end_date
        )
        .group_by(func.date(Workout.date))
        .all()
    )
    return stats


@router.get("/category")
def get_category_statistics(category_id: int, db: Session = Depends(get_db)):
    """
    특정 운동 카테고리에 대한 통계 API
    - 해당 카테고리에 속한 전체 운동 기록에 대해
      평균 중량과 평균 반복 횟수를 계산합니다.
    """
    stats = (
        db.query(
            func.avg(Workout.weight).label("avg_weight"),
            func.avg(Workout.reps).label("avg_reps")
        )
        .filter(Workout.category_id == category_id)
        .first()
    )
    if not stats:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No statistics found for this category")
    return stats
