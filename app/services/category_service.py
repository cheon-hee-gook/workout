from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate


def get_category_by_name(db: Session, name: str):
    """
    카테고리 이름으로 기존 카테고리 조회 (중복 체크 용도)
    """
    return db.query(Category).filter(Category.name == name).first()


def create_category(db: Session, category_data: CategoryCreate):
    """
    새로운 운동 카테고리를 DB에 저장합니다.
    """
    new_category = Category(name=category_data.name, description=category_data.description)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_categories(db: Session):
    """
    모든 운동 카테고리를 조회합니다.
    """
    return db.query(Category).all()


def update_category(db: Session, category_id: int, category_data: CategoryCreate):
    """
    기존 카테고리 정보를 업데이트합니다.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        category.name = category_data.name
        category.description = category_data.description
        db.commit()
        db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    """
    운동 카테고리를 삭제합니다.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category
