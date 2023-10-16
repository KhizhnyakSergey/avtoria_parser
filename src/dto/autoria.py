from typing import List, Optional, Dict, Any
from datetime import datetime

from pydantic import BaseModel


class TicketPhoneEncrypted(BaseModel):
    hash: str
    expires: int


class TicketShort(BaseModel):
    isAutoBuy: bool
    categoryId: int
    autoId: int
    userId: int
    markaId: int
    modelId: int
    bodyId: int
    stateId: int
    marka: str
    model: str
    year: int
    yearLetter: str
    yearRaceSlash: str
    version: str
    city: str
    cityLocative: str
    photoBig: str
    photoMedium: str
    photoSmall: str
    photoRiaSmall: str
    photoPath: str
    link: str
    race: str
    currency: str
    currencyId: int
    priceFromText: str
    type: str
    typeName: str
    USD: str
    EUR: str
    UAH: str
    level: int
    levelExpire: str
    topType: str
    userSecure: Optional[TicketPhoneEncrypted] = None 
    

class SellerPhones(BaseModel):
    phones: Optional[List[str]] = None


class DBData(BaseModel):
    ticket_id: int
    url: str
    title: str
    price: int
    odometer: Optional[int] = None
    username: Optional[str] = None
    phone_numbers: Optional[List[str]] = None
    image_url: str
    images_count: Optional[int] = None
    car_number: Optional[str] = None
    car_vin: Optional[str] = None
    found_date: datetime
    is_active: bool
