from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel 

from src.dto.phone import PhoneDTO


class TicketCreate(BaseModel):
    
    ticket_id: int 
    url: str
    title: str
    price: int
    odometer: Optional[int] = None
    username: Optional[str] = None
    image_url: str
    images_count: Optional[int] = None
    car_number: Optional[str] = None
    car_vin: Optional[str] = None
    found_date: datetime
    is_active: bool 


class TicketDTO(BaseModel):

    ticket_id: int 
    url: str
    title: str
    price: int
    odometer: Optional[int] = None
    username: Optional[str] = None
    image_url: str
    images_count: Optional[int] = None
    car_number: Optional[str] = None
    car_vin: Optional[str] = None
    found_date: datetime
    is_active: bool 
    phones: List[PhoneDTO] = []
    