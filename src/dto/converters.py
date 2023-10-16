import re
from typing import Dict, Any, List, Optional

from src.dto.autoria import (
    TicketPhoneEncrypted, 
    TicketShort, 
    SellerPhones
)
from src.database.models.ticket import Ticket
from src.dto.ticket import TicketDTO
from src.database.models.phone import Phone
from src.dto.phone import PhoneDTO


def convert_data_to_ticket_short(data: Dict[str, Any]) -> TicketShort:
    user_secure = data.pop('userSecure', None)
    return TicketShort(
        userSecure=TicketPhoneEncrypted(**user_secure) if user_secure else None,
        **data
    )

def convert_data_to_seller_phones(data: Dict[str, Any]) -> SellerPhones:
    phones = data.pop('phones', None)
    pattern = r'\(|\)| '
    stripped = [f"+38{''.join(re.split(pattern, phone['phoneFormatted']))}" for phone in phones]
    return SellerPhones(
        phones=stripped
    )

def convert_phone_model_to_dto(phone: Phone) -> PhoneDTO:
    return PhoneDTO(
        phone_number=phone.phone_number,
        ticket_id=phone.ticket_id
    )


def convert_ticket_model_to_dto(ticket: Ticket) -> TicketDTO:
    phones = []
    if "phones" in ticket.as_dict():
        phones = ticket.phones

    return TicketDTO(
        ticket_id=ticket.ticket_id,
        url=ticket.url,
        title=ticket.title,
        price=ticket.price,
        odometer=ticket.odometer,
        username=ticket.username,
        image_url=ticket.image_url,
        images_count=ticket.images_count,
        car_number=ticket.car_number,
        car_vin=ticket.car_vin,
        found_date=ticket.found_date,
        is_active=ticket.is_active,
        phones=phones
    )