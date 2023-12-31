import abc
from typing import Generic, Type, TypeAlias

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories.crud import CRUDRepository, Model 


class BaseRepository(abc.ABC, Generic[Model]):
    
    model: Type[Model]
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crud = CRUDRepository(session, self.model)


TypeRepository: TypeAlias = BaseRepository[Model]