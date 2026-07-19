from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.device_tracking import DeviceTracking
from app.db.session import get_db
from app.services.tokens import verify_token


# class JWTBearer(HTTPBearer):
#     async def __call__(self, request: Request):
#         auth = await super().__call__(request)
#         token = auth.credentials
#         payload = verify_token(token)
#         if payload is None:
#             raise HTTPException(status_code=401, detail="Invalid or expired access token")
#         return payload
    

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict | None:
        auth: HTTPAuthorizationCredentials | None = await super().__call__(request)

        if auth is None: return None

        payload = verify_token(auth.credentials)

        if payload is None:
            if self.auto_error:
                raise HTTPException(status_code=401, detail="Invalid or expired access token")
            return None

        return payload


def get_payload(payload = Depends(JWTBearer()), db: Session = Depends(get_db)):
    if not _validate_device(payload, db):
        raise HTTPException(status_code=401, detail="Session not found. Please log in again")
    return payload


def get_optional_payload(payload = Depends(JWTBearer(auto_error=False)), db: Session = Depends(get_db)):
    if not _validate_device(payload, db):
        return None
    return payload


def _validate_device(payload: dict | None, db: Session) -> bool:
    if payload is None: return False

    device_id = payload.get("device_id")
    access_version = payload.get("access_version")

    if device_id is None or access_version is None:
        return False
    
    db_device = db.query(DeviceTracking).filter(
        DeviceTracking.device_id == device_id
    ).first()

    return bool(db_device and db_device.access_version == access_version)