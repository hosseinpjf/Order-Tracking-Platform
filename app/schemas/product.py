from pydantic import BaseModel, Field
from uuid import UUID
from typing import List
from app.models.product import ProductTags

class ImageSchema(BaseModel):
    url: str
    position: int

class CreateProduct(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    price: int = Field(..., gt=0)
    discount_percent: int = Field(default=0, ge=0, le=100)
    category_id: UUID
    images: List[ImageSchema] = Field(default_factory=list)
    is_available: bool = True
    tags: ProductTags
    prepare_time: int = Field(..., gt=0)