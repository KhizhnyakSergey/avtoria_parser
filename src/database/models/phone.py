from typing import Optional, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String,
    ForeignKey,
    Integer
)

from src.database.models.base import ModelWithTime, Base, ModelWithID


if TYPE_CHECKING:
    from src.database.models.ticket import Ticket


class Phone(Base, ModelWithTime, ModelWithID):

    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey("ticket.ticket_id"))
    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="phones")