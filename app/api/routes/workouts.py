from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.workout import WorkoutCreate, WorkoutResponse
from app.services.workout_service import create_workout, get_workout, get_workouts, update_workout, delete_workout
from app.db.session import get_db
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=WorkoutResponse)
def create_new_workout(
        workout: WorkoutCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # 로그인한 사용자 정보 획득
):
    """
    새로운 운동 기록을 생성합니다.
    - 요청 시 JWT 토큰을 통해 인증된 사용자만 접근할 수 있습니다.
    - current_user는 인증된 사용자 정보입니다.
    """
    # 요청 데이터의 user_id가 current_user.id와 일치하는지 검증
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to create workout for other users")

    new_workout = create_workout(db, workout)
    return new_workout


@router.get("/{workout_id}", response_model=WorkoutResponse)
def read_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 인증된 사용자만 조회 가능
):
    """
    특정 운동 기록을 조회합니다.
    - 인증된 사용자만 접근할 수 있습니다.
    """
    workout = get_workout(db, workout_id)
    if not workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    # 추가로, 조회한 운동 기록이 current_user와 관련된 것인지 확인할 수 있습니다.
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this workout")
    return workout


@router.get("/", response_model=List[WorkoutResponse])
def read_workouts(
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # 인증된 사용자만 접근
):
    """
    전체 운동 기록 또는 특정 사용자의 기록을 조회합니다.
    - user_id 필터링 시에도 current_user의 정보와 비교할 수 있습니다.
    """
    # 인증된 사용자가 자신의 기록만 조회하도록 제한
    if user_id is None or user_id != current_user.id:
        user_id = current_user.id
    workouts = get_workouts(db, user_id)
    return workouts


@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_existing_workout(
        workout_id: int,
        workout: WorkoutCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    운동 기록을 업데이트합니다.
    - 인증된 사용자만 접근할 수 있으며, 자신의 기록만 수정 가능해야 합니다.
    """
    existing_workout = get_workout(db, workout_id)
    if not existing_workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    if existing_workout.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this workout")

    updated = update_workout(db, workout_id, workout)
    return updated


@router.delete("/{workout_id}", response_model=WorkoutResponse)
def delete_existing_workout(
        workout_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    운동 기록을 삭제합니다.
    - 인증된 사용자만 접근할 수 있으며, 자신의 기록만 삭제 가능해야 합니다.
    """
    existing_workout = get_workout(db, workout_id)
    if not existing_workout:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    if existing_workout.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this workout")

    deleted = delete_workout(db, workout_id)
    return deleted
