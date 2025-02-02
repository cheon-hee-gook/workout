from fastapi import FastAPI
from app.api.routes import users, workouts, categories, auth, statistics
from app.db.session import engine
from app.db.base import Base

# 모든 모델의 테이블 생성 (개발 초기 단계에만 사용)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workout Management API")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(workouts.router, prefix="/workouts", tags=["Workouts"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(statistics.router, prefix="/statistics", tags=["Statistics"])

@app.get("/")
def read_root():
    return {"message": "Workout Management API is running!"}
