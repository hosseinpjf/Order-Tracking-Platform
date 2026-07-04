from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.jwt_bearer import get_payload
from app.schemas.product import CreateProduct
from app.models.product import Product
from app.middleware.exception_handler import response_handler

router = APIRouter(prefix="/product", tags=["Product"])

@router.post("/create")
def create_product(data: CreateProduct, payload = Depends(get_payload), db: Session = Depends(get_db)):
    try:
        new_product = Product(
            title = data.title,
            description = data.description,
            price = data.price,
            discount_percent = data.discount_percent,
            category_id = data.category_id,
            images = [img.dict() for img in data.images],
            is_available = data.is_available,
            tags = [tag.value for tag in data.tags],
            prepare_time = data.prepare_time
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return response_handler(
            status=True,
            message="Product created successfully",
            data={
                "id": new_product.id,
                "title": new_product.title,
                "description": new_product.description,
                "price": new_product.price,
                "discount_percent": new_product.discount_percent,
                "category_id": new_product.category_id,
                "images": new_product.images,
                "is_available": new_product.is_available,
                "likes": new_product.likes,
                "tags": new_product.tags,
                "prepare_time": new_product.prepare_time,
                "created_at": new_product.created_at,
                "updated_at": new_product.updated_at
            },
            status_code=201
        )
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Registration failed")
