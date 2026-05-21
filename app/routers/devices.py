from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.device import Device

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/")
def get_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()


@router.get("/{device_id}")
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.post("/")
def create_device(payload: dict, db: Session = Depends(get_db)):
    device = Device(**payload)

    db.add(device)
    db.commit()
    db.refresh(device)

    return device


@router.put("/{device_id}")
def update_device(device_id: int, payload: dict, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    for key, value in payload.items():
        setattr(device, key, value)

    db.commit()
    db.refresh(device)

    @router.delete("/{device_id}")
    def delete_device(device_id: int, db: Session = Depends(get_db)):
        device = db.query(Device).filter(Device.id == device_id).first()

        if not device:
            raise HTTPException(status_code=404, detail="Device not found")

        db.delete(device)
        db.commit()

        return {"message": "Device deleted successfully"}