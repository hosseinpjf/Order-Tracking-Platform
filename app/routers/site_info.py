from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.orm.attributes import flag_modified
import uuid
from app.db.session import get_db
from app.services.jwt_bearer import get_payload
from app.middleware.exception_handler import response_handler
from app.models.site_info import SiteInfo
from app.schemas.site_info import CreateSiteInfo, UpdateSiteInfo
from app.utils.site_info_update import update_list, update_section


router = APIRouter(prefix="/info", tags=["Site Info"])

FIELDS_WITH_LIST_DATA = ["slogans", "phones", "links", "working_hours", "settings", "today_suggestions"]
FIELDS_WITH_DICT_DATA = ["hero", "footer", "about_us", "contact_us"]
FIELDS_WITH_SIMPLE_DATA = ["name", "logo", "address", "table_reservation_time", "location"]

@router.post("/")
def create_info(data: CreateSiteInfo, payload = Depends(get_payload), db: Session = Depends(get_db)):
    try:
        if payload["role"] != "admin":
            raise HTTPException(status_code=403, detail="Access denied")

        db_site_info = db.query(SiteInfo).first()
        if not db_site_info:
            db_site_info = SiteInfo()
            db.add(db_site_info)
            db.flush()

        create_data = data.model_dump(
            mode="json",
            exclude_unset=True,
            exclude_none=True
        )

        for key, value in create_data.items():

            if key in FIELDS_WITH_SIMPLE_DATA:
                setattr(db_site_info, key, value)
                continue

            if key in FIELDS_WITH_LIST_DATA:
                current_value = list(getattr(db_site_info, key) or [])

                for item in value:
                    item["id"] = uuid.uuid4().hex
                    if key in ("slogans", "phones", "links", "today_suggestions"):
                        item.setdefault("is_visible", True)
                    current_value.append(item)

                setattr(db_site_info, key, current_value)
                flag_modified(db_site_info, key)
                continue

            if key in FIELDS_WITH_DICT_DATA:
                current_section = dict(getattr(db_site_info, key) or {})

                for section_key, section_value in value.items():
                    if section_key in ("images", "buttons"):
                        current_items = current_section.get(section_key, [])

                        for item in section_value:
                            item["id"] = uuid.uuid4().hex
                            current_items.append(item)

                        current_section[section_key] = current_items
                    else:
                        current_section[section_key] = section_value

                setattr(db_site_info, key, current_section)
                flag_modified(db_site_info, key)
                continue

        db.commit()
        db.refresh(db_site_info)

        return response_handler(
            status=True,
            message="Data created successfully",
            data=None,
            status_code=201
        )
    except HTTPException as http_error:
        db.rollback()
        raise http_error
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Site info create failed")


@router.patch("/")
def update_info(data: UpdateSiteInfo, payload = Depends(get_payload), db: Session = Depends(get_db)):
    try:
        if payload["role"] != "admin":
            raise HTTPException(status_code=403, detail="Access denied")

        db_site_info = db.query(SiteInfo).first()
        if not db_site_info:
            raise HTTPException(status_code=404, detail="Site info not found")

        update_data = data.model_dump(
            mode="json",
            exclude_unset=True,
            exclude_none=True,
        )

        for key, value in update_data.items():

            if key in FIELDS_WITH_SIMPLE_DATA:
                setattr(db_site_info, key, value)
                continue

            if key in FIELDS_WITH_LIST_DATA:
                current_value = getattr(db_site_info, key) or []
                setattr(db_site_info, key, update_list(current_value, value))
                flag_modified(db_site_info, key)
                continue

            if key in FIELDS_WITH_DICT_DATA:
                current_section = getattr(db_site_info, key) or {}
                setattr(db_site_info, key, update_section(current_section, value))
                flag_modified(db_site_info, key)
                continue

        db.commit()
        db.refresh(db_site_info)

        return response_handler(
            status=True,
            message="Data updated successfully",
            data=None,
            status_code=200
        )
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Site info update failed")


# from app.db.session import SessionLocal
# from app.models.site_info import SiteInfo
# def delete_site_info():
#     db = SessionLocal()
#     try:
#         site_info = db.query(SiteInfo).filter(SiteInfo.id == "1").first()
#         if not site_info:
#             print("site_info not found")
#             return
#         db.delete(site_info)
#         db.commit()
#         print("site_info deleted with cascade")
#     except:
#         db.rollback()
#         raise
#     finally:
#         db.close()
# delete_site_info()
