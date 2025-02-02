# Workout Management API

이 프로젝트는 **FastAPI**를 사용하여 개발한 운동 관리 웹 애플리케이션의 백엔드입니다.  
JWT 기반 인증, 사용자 관리, 운동 기록 관리, 운동 카테고리 관리, 통계 기능 등 다양한 기능을 포함하고 있으며, RESTful API를 제공합니다.

## 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 실행](#설치-및-실행)
- [환경 변수 설정](#환경-변수-설정)
- [API 문서](#api-문서)
- [테스트 방법](#테스트-방법)

## 프로젝트 개요

이 백엔드 애플리케이션은 운동 기록과 관련된 모든 데이터를 관리하기 위한 REST API를 제공합니다.  
사용자는 회원가입 및 로그인을 통해 JWT 토큰을 받고, 이를 이용해 자신의 운동 기록과 카테고리를 관리하며, 주간/월간 통계를 조회할 수 있습니다.

## 주요 기능

- **사용자 관리**
  - 회원가입, 로그인 및 JWT 인증
  - 프로필 수정 및 탈퇴 기능 (추후 확장 가능)
- **운동 기록 관리**
  - 운동 기록 생성, 조회, 수정, 삭제(CRUD)
  - 운동 기록에 포함된 정보: 운동 종류, 세트 수, 반복 횟수, 중량, 메모 등
- **운동 카테고리 관리**
  - 다양한 운동 종목(예: 스쿼트, 벤치프레스 등) 관리
- **통계 기능**
  - 주간 및 월간 운동 기록 통계 (운동 횟수, 평균 중량, 평균 반복 횟수)
  - 특정 카테고리에 대한 통계 조회
- **인증**
  - OAuth2PasswordBearer를 이용한 JWT 기반 인증

## 기술 스택

- **Backend Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **인증:** JWT (PyJWT, OAuth2PasswordBearer)
- **환경 변수 관리:** python-dotenv
- **서버 실행:** Uvicorn

## 프로젝트 구조
```bash
workout_app/ 
├── app/ │ 
   ├── api/ │ 
   │ ├── routes/ │ │ 
   │ │ ├── users.py # 사용자 관리 관련 API 엔드포인트 │  
   │ │ ├── workouts.py # 운동 기록 관리 API 엔드포인트 │  
   │ │ ├── categories.py # 운동 카테고리 관리 API 엔드포인트 │ 
   │ │ ├── auth.py # 인증 (로그인) API 엔드포인트 │ 
   │ │ ├── statistics.py # 통계 기능 API 엔드포인트 │ 
   │ ├── dependencies.py # JWT 토큰 검증 및 현재 사용자 의존성 함수 │
   ├── core/ │ 
   │ ├── config.py # 환경 변수 및 설정 관리 │ 
   │ ├── security.py # 비밀번호 해싱 및 JWT 토큰 생성/검증 로직 │ 
   ├── models/ │ 
   │ ├── user.py # 사용자 모델 (SQLAlchemy ORM) │ 
   │ ├── workout.py # 운동 기록 모델 │ 
   │ ├── category.py # 운동 카테고리 모델 │ 
   ├── schemas/ │ 
   │ ├── user.py # 사용자 요청/응답 스키마 (Pydantic) │ 
   │ ├── workout.py # 운동 기록 관련 스키마 │ 
   │ ├── category.py # 카테고리 관련 스키마 │ 
   ├── services/ │ 
   │ ├── user_service.py # 사용자 관련 비즈니스 로직 │ 
   │ ├── workout_service.py # 운동 기록 관련 로직 │ 
   │ ├── category_service.py # 카테고리 관련 로직 │ 
   ├── db/ │ 
   │ ├── base.py # SQLAlchemy Base 선언   │
   │ ├── session.py # 데이터베이스 세션 관리  │
   ├── tests/ # 유닛 테스트 코드 
   ├── .env # 환경 변수 파일 (DB URL, JWT 시크릿) 
   ├── requirements.txt # 필요 패키지 목록 
   ├── main.py # FastAPI 애플리케이션 진입점 (라우터 등록 및 실행)
```

## 설치 및 실행

1. **프로젝트 클론 및 디렉토리 이동**

   ```bash
   git clone <repository-url>
   cd workout_app
   ```
   
2. **가상 환경 생성 및 활성화**

   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **필수 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

4. **환경 변수 설정**

    ```bash
    DATABASE_URL=postgresql://user:password@localhost/dbname
    JWT_SECRET_KEY=your-secret-key
    JWT_EXPIRE_MINUTES=60
    ```

5. **데이터베이스 초기화**

개발 초기 단계에서는 main.py 내 Base.metadata.create_all(bind=engine)을 통해 테이블을 생성할 수 있습니다.
(운영 환경에서는 Alembic 등 마이그레이션 도구를 사용하는 것이 좋습니다.)

6. **서버 실행**

   ```bash
   uvicorn main:app --reload
   ```

서버는 기본적으로 http://localhost:8000에서 실행됩니다.

## 환경 변수 설정
- DATABASE_URL: 데이터베이스 연결 URL (PostgreSQL)
- JWT_SECRET_KEY: JWT 토큰 생성에 사용되는 시크릿 키
- JWT_EXPIRE_MINUTES: JWT 토큰 만료 시간(분)

## API 문서
FastAPI는 자동으로 API 문서를 생성합니다.
 - Swagger UI: http://localhost:8000/docs
 - ReDoc: http://localhost:8000/redoc

API 엔드포인트, 요청/응답 형식, 예시 등을 확인할 수 있습니다.

## 테스트 방법
### Postman을 활용한 API 테스트
1. 회원가입 테스트:
   - URL: POST http://localhost:8000/users/signup
   - Body (JSON):
   - ```json
     {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "yourpassword"
     }
     ```

2. 로그인 테스트:
   - URL: POST http://localhost:8000/auth/login
   - Body (x-www-form-urlencoded):
     - username: testuser 
     - password: yourpassword

   로그인 성공 시 응답으로 JWT 토큰이 반환됩니다.


3. JWT 인증을 통한 보호된 엔드포인트 접근:

    예: 운동 기록 생성 
   - URL: POST http://localhost:8000/workouts/
   - Header: Authorization: Bearer <JWT 토큰>
   - Body (JSON):
   - ```json
     {
        "user_id": 1,
        "category_id": 2,
        "sets": 3,
        "reps": 10,
        "weight": 50.0,
        "note": "첫 운동 기록"
     }
     ```

다른 엔드포인트들도 Postman 또는 Swagger UI를 통해 테스트 가능합니다.
