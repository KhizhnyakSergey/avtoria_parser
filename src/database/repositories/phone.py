from typing import (
    Type,
    List,
)

from src.database.repositories.base import BaseRepository
from src.database.models.phone import Phone
from src.dto.phone import PhoneCreate, PhoneDTO
from src.dto.converters import convert_phone_model_to_dto


class PhoneRepository(
    BaseRepository[Phone], 
):

    model: Type[Phone] = Phone

    async def create_many(self, query: List[PhoneCreate]) -> List[PhoneDTO]:

        data = [dto.model_dump(exclude_none=True) for dto in query]
        result = await self._crud.create_many(data)

        return [convert_phone_model_to_dto(model) for model in result]
    
