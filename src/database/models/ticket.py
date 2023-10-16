from datetime import datetime
from typing import Optional, TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    Boolean,
    Integer,
    True_,
    DateTime,
)

from src.database.models.base import ModelWithTime, Base


if TYPE_CHECKING:
    from src.database.models.phone import Phone

class Ticket(Base, ModelWithTime):

    ticket_id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    odometer: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    images_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    car_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    car_vin: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    found_date: Mapped[datetime] = mapped_column(DateTime(True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=True_())
    phones: Mapped[List["Phone"]] = relationship("Phone", back_populates="ticket")
    

