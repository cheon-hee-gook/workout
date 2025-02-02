from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import create_category, get_categories, update_category, delete_category, get_category_by_name
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=CategoryResponse)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """
    새로운 운동 카테고리를 생성합니다.
    """
    # 중복 카테고리 여부 확인
    existing = get_category_by_name(db, category.name)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    new_category = create_category(db, category)
    return new_category


@router.get("/", response_model=List[CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    """
    모든 운동 카테고리를 조회합니다.
    """
    categories = get_categories(db)
    return categories


@router.put("/{category_id}", response_model=CategoryResponse)
def update_existing_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    """
    운동 카테고리를 업데이트합니다.
    """
    updated = update_category(db, category_id, category)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return updated


@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_existing_category(category_id: int, db: Session = Depends(get_db)):
    """
    운동 카테고리를 삭제합니다.
    """
    deleted = delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return deleted
