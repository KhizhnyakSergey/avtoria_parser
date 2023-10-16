from typing import Optional

from pydantic import BaseModel 


class PhoneCreate(BaseModel):
    
    phone_number: Optional[str] = None
    ticket_id: int

class PhoneDTO(BaseModel):
    
    phone_number: Optional[str] = None
    ticket_id: int