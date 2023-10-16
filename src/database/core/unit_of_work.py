from __future__ import annotations
from types import TracebackType
from typing import Optional, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from src.database.exceptions import CommitError, RollbackError


class UnitOfWork:
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._transaction: Optional[AsyncSessionTransaction] = None
    
    async def __aenter__(self) -> UnitOfWork: 
        await self._create_transaction()
        return self
    
    async def __aexit__(
            self, 
            exc_type: Optional[Type[BaseException]], 
            exc_value: Optional[BaseException], 
            traceback: Optional[TracebackType]
    ) -> None:
        
        if self._transaction:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
                
        await self._session.close()

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err
        

    async def _create_transaction(self) -> None:
        
        if not self._session.in_transaction() and self._session.is_active:
            self._transaction = await self._session.begin()