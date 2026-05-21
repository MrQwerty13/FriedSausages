from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.config_snapshot import ConfigSnapshot

router = APIRouter(prefix="/configs", tags=["Configs"])


@router.get("/")
def get_snapshots(db: Session = Depends(get_db)):
    return db.query(ConfigSnapshot).all()


@router.get("/{snapshot_id}")
def get_snapshot(snapshot_id: int, db: Session = Depends(get_db)):
    snapshot = (
        db.query(ConfigSnapshot)
        .filter(ConfigSnapshot.id == snapshot_id)
        .first()
    )

    if not snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")

    return snapshot


@router.post("/")
def create_snapshot(payload: dict, db: Session = Depends(get_db)):
    snapshot = ConfigSnapshot(**payload)

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot