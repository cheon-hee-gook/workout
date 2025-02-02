from fastapi import FastAPI
from app.api.routes import users

app = FastAPI(title="Workout Management API")

# 각 라우터들을 포함
app.include_router(users.router, prefix="/users", tags=["Users"])
# app.include_router(workouts.router, prefix="/workouts", tags=["Workouts"])
# app.include_router(categories.router, prefix="/categories", tags=["Categories"])
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(statistics.router, prefix="/statistics", tags=["Statistics"])

# 루트 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Workout Management API is running!"}
