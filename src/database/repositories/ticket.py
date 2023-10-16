from typing import (
    Optional,
    Type,
    List
)

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.repositories.base import BaseRepository
from src.database.models.ticket import Ticket
from src.dto.ticket import TicketCreate, TicketDTO
from src.dto.converters import convert_ticket_model_to_dto


class TicketRepository(
    BaseRepository[Ticket], 
):

    model: Type[Ticket] = Ticket

    async def create(self, query: TicketCreate) -> Optional[TicketDTO]:

        result = await self._crud.create(**query.model_dump(exclude_none=True))
        if not result:
            return None
        
        return convert_ticket_model_to_dto(result)

    async def create_many(self, query: List[TicketCreate]) -> List[TicketDTO]:

        data = [dto.model_dump(exclude_none=True) for dto in query]
        result = await self._crud.create_many(data)

        return [convert_ticket_model_to_dto(model) for model in result]
    
    async def select(self, ticket_id: int) -> Optional[TicketDTO]:

        result = await self._crud.select(self.model.ticket_id==ticket_id)
        if not result:
            return None
        
        return convert_ticket_model_to_dto(result)
    
    async def select_with_phones(self, ticket_id: int) -> Optional[TicketDTO]:

        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.phones) 
            )
            .where(self.model.ticket_id==ticket_id)
        )
        result = (await self._session.execute(stmt)).scalars().first()

        return result


    