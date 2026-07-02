from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.device_tracking import DeviceTracking
from app.middleware.exception_handler import response_handler
from app.services.jwt_bearer import JWTBearer

router = APIRouter(prefix="/device", tags=["Device"])

@router.delete("/delete/{device_id}")
def delete_device(device_id: str, payload = Depends(JWTBearer()), db: Session = Depends(get_db)):

    db_device = db.query(DeviceTracking).filter(DeviceTracking.id == device_id).first()

    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if payload["role"] != "admin" and payload["sub"] != db_device.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    db_devices_count = db.query(DeviceTracking).filter(DeviceTracking.user_id == db_device.user_id).count()

    if db_devices_count <= 1:
        raise HTTPException(status_code=409, detail="User must have at least one device")
    
    db.delete(db_device)
    db.commit()
    
    return response_handler(
        status=True,
        message="Device deleted successfully",
        data=None,
        status_code=200
    )