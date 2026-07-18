from sqlalchemy.orm import Session
import uuid
from app.models.site_info import SiteInfo, SiteInfoSettings, DaysWeek
from sqlalchemy.orm.attributes import flag_modified


def init_settings(db: Session):
    try:
        site_info = db.query(SiteInfo).first()

        if not site_info:
            site_info = SiteInfo(settings=[], working_hours=[])
            db.add(site_info)
            db.flush()

        current_settings = list(site_info.settings or [])
        valid_capabilities = {setting.value for setting in SiteInfoSettings}
        existing_capabilities = {
            s.get("capability")
            for s in current_settings
            if isinstance(s, dict)
        }

        changed = False

        for setting in SiteInfoSettings:
            if setting.value not in existing_capabilities:
                current_settings.append({
                    "id": uuid.uuid4().hex,
                    "capability": setting.value,
                    "enabled": True
                })
                changed = True

        filtered_settings = [
            s
            for s in current_settings
            if isinstance(s, dict)
            and s.get("capability") in valid_capabilities
        ]
        if len(filtered_settings) != len(current_settings):
            current_settings = filtered_settings
            changed = True

        if changed:
            site_info.settings = current_settings
            flag_modified(site_info, "settings")

        db.commit()

    except Exception:
        db.rollback()
        raise



DEFAULT_OPEN_TIME = "09:00:00"
DEFAULT_CLOSE_TIME = "23:00:00"
CLOSED_DAYS = {DaysWeek.friday.value}

def init_working_hours(db: Session):
    try:
        site_info = db.query(SiteInfo).first()

        if not site_info:
            site_info = SiteInfo(settings=[], working_hours=[])
            db.add(site_info)
            db.flush()

        current_days = list(site_info.working_hours or [])
        valid_days = {day.value for day in DaysWeek}
        existing_days = {
            d.get("day")
            for d in current_days
            if isinstance(d, dict)
        }

        changed = False

        for day in DaysWeek:
            if day.value not in existing_days:
                is_closed = day.value in CLOSED_DAYS
                current_days.append({
                    "id": uuid.uuid4().hex,
                    "day": day.value,
                    "open_time": None if is_closed else DEFAULT_OPEN_TIME,
                    "close_time": None if is_closed else DEFAULT_CLOSE_TIME,
                    "is_closed": is_closed,
                })
                changed = True

        filtered_days = [
            s
            for s in current_days
            if isinstance(s, dict)
            and s.get("day") in valid_days
        ]
        if len(filtered_days) != len(current_days):
            current_days = filtered_days
            changed = True

        if changed:
            site_info.working_hours = current_days
            flag_modified(site_info, "working_hours")

        db.commit()

    except Exception:
        db.rollback()
        raise