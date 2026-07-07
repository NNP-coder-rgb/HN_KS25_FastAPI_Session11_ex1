
from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class ParkingModel(Base):
    __tablename__ = "parking_slots"

    slot_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    slot_code = Column(String(50), unique=True, nullable=False)
    zone_name = Column(String(255), nullable=False)
    max_weight = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)