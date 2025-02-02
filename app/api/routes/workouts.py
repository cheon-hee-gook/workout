from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.workout import WorkoutCreate, WorkoutResponse
from app.services.workout_service import create_workout, get_workout, get_workouts, update_workout, delete_workout
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=WorkoutResponse)
def create_new_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    """
    새로운 운동 기록을 생성합니다.
    """
    new_workout = create_workout(db, workout)
    return new_workout


@router.get("/{workout_id}", response_model=WorkoutResponse)
def read_workout(workout_id: int, db: Session = Depends(get_db)):
    """
    특정 운동 기록을 조회합니다.
    """
    workout = get_workout(db, workout_id)
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    return workout

@router.get("/", response_model=List[WorkoutResponse])
def read_workouts(user_id: int = None, db: Session = Depends(get_db)):
    """
    전체 운동 기록 또는 특정 사용자의 기록을 조회합니다.
    """
    workouts = get_workouts(db, user_id)
    return workouts


@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_existing_workout(workout_id: int, workout: WorkoutCreate, db: Session = Depends(get_db)):
    """
    운동 기록을 업데이트합니다.
    """
    updated = update_workout(db, workout_id, workout)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    return updated


@router.delete("/{workout_id}", response_model=WorkoutResponse)
def delete_existing_workout(workout_id: int, db: Session = Depends(get_db)):
    """
    운동 기록을 삭제합니다.
    """
    deleted = delete_workout(db, workout_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    return deleted
