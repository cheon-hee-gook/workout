from sqlalchemy.orm import Session
from app.models.workout import Workout
from app.schemas.workout import WorkoutCreate


def create_workout(db: Session, workout_data: WorkoutCreate):
    """
    새로운 운동 기록을 DB에 저장합니다.
    """
    workout = Workout(
        user_id=workout_data.user_id,
        category_id=workout_data.category_id,
        sets=workout_data.sets,
        reps=workout_data.reps,
        weight=workout_data.weight,
        note=workout_data.note
    )
    db.add(workout)      # 새 운동 기록 추가
    db.commit()          # DB에 저장
    db.refresh(workout)  # 최신 정보를 workout 객체에 업데이트
    return workout


def get_workout(db: Session, workout_id: int):
    """
    운동 기록 ID로 특정 기록을 조회합니다.
    """
    return db.query(Workout).filter(Workout.id == workout_id).first()


def get_workouts(db: Session, user_id: int = None):
    """
    전체 운동 기록 또는 특정 사용자의 운동 기록을 조회합니다.
    """
    query = db.query(Workout)
    if user_id:
        query = query.filter(Workout.user_id == user_id)
    return query.all()


def update_workout(db: Session, workout_id: int, workout_data: WorkoutCreate):
    """
    기존 운동 기록을 업데이트합니다.
    """
    workout = get_workout(db, workout_id)
    if workout:
        workout.category_id = workout_data.category_id
        workout.sets = workout_data.sets
        workout.reps = workout_data.reps
        workout.weight = workout_data.weight
        workout.note = workout_data.note
        db.commit()
        db.refresh(workout)
    return workout


def delete_workout(db: Session, workout_id: int):
    """
    운동 기록을 삭제합니다.
    """
    workout = get_workout(db, workout_id)
    if workout:
        db.delete(workout)
        db.commit()
    return workout
