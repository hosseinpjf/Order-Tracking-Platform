from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from app.db.session import get_db
from app.services.jwt_bearer import get_payload, get_optional_payload
from app.middleware.exception_handler import response_handler
from app.models.site_content import SiteContent, SiteContentType
from app.schemas.site_content import CreateSiteContent, OutSiteContent, UpdateSiteContent
from app.utils.delete_file import delete_file, delete_files
from app.utils.get_site_info import get_settings


router = APIRouter(prefix="/contents", tags=["Site Contents"])


@router.post("/{content_type}")
def create_contents(content_type: SiteContentType, data: CreateSiteContent, payload = Depends(get_payload), db: Session = Depends(get_db)):
    try:
        if payload["role"] != "admin":
            raise HTTPException(status_code=403, detail="Access denied")
        
        create_data = data.model_dump(
            mode="json",
            exclude_unset=True,
            exclude_none=True
        )

        new_content = SiteContent(type = content_type)

        for key, value in create_data.items():
            setattr(new_content, key, value)

        db.add(new_content)
        db.commit()
        db.refresh(new_content)

        return response_handler(
            status=True,
            message="Content created successfully",
            data=OutSiteContent.model_validate(new_content).model_dump(),
            status_code=201
        )
    except HTTPException as http_error:
        db.rollback()
        raise http_error
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Site content create failed")


@router.patch("/{content_id}")
def update_content(content_id: str, data: UpdateSiteContent, payload = Depends(get_payload), db: Session = Depends(get_db)):
    try:
        if payload["role"] != "admin":
            raise HTTPException(status_code=403, detail="Access denied")

        db_content = db.query(SiteContent).filter(SiteContent.id == content_id).first()
        if not db_content:
            raise HTTPException(status_code=404, detail="Content not found")
        
        old_files = set()
        new_files = set()

        update_data = data.model_dump(
            mode="json",
            exclude_unset=True,
            exclude_none=True
        )

        for field in ("images", "icons"):
            if field in update_data:
                old_files.update(item["url"] for item in (getattr(db_content, field) or []) if item.get("url"))
                new_files.update(item["url"] for item in update_data[field] if item.get("url"))

        for key, value in update_data.items():
            setattr(db_content, key, value)

        for field in ("images", "icons", "buttons", "content"):
            if field in update_data:
                flag_modified(db_content, field)

        db.commit()
        db.refresh(db_content)

        delete_files_list = list(old_files - new_files)
        if delete_files_list:
            delete_files(delete_files_list)

        return response_handler(
            status=True,
            message="Content updated successfully",
            data=OutSiteContent.model_validate(db_content).model_dump(),
            status_code=200
        )
    except HTTPException as http_error:
        db.rollback()
        raise http_error
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Site content update failed")

