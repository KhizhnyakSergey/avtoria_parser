from src.database.repositories.ticket import TicketRepository
from src.database.repositories.phone import PhoneRepository


__all__ = (
    "TicketRepository",
    "PhoneRepository",
)

REPOSITORIES = (
    TicketRepository, 
    PhoneRepository,
)
