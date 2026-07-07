from sqlalchemy.orm import Session
from model import ParkingModel
from fastapi import HTTPException, status

def create_parking(db: Session, slot_code: str, zone_name: str, max_weight: int, is_available: bool):
    parking = db.query(ParkingModel).filter(ParkingModel.slot_code == slot_code).first()

    if parking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parking slot not found!"
        )

    new_parking = ParkingModel(
        slot_code = slot_code,
        zone_name = zone_name,
        max_weight = max_weight,
        is_available = is_available
    )
    try:
        db.add(new_parking)
        db.commit()
        db.refresh(new_parking)

        return new_parking
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

def get_parking_slots(db: Session):
    parkings = db.query(ParkingModel).all()
    return parkings

def get_parking_by_id(db: Session, slot_id: int):
    parking = db.query(ParkingModel).filter(ParkingModel.slot_id == slot_id).first()

    if not parking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking Slot Not Found!"
        )
    return parking
    