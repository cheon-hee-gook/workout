from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """새로운 카테고리 생성 시 사용되는 스키마"""
    pass


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
