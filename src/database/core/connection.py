import pytz
from datetime import datetime
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncEngine, 
    async_sessionmaker, 
    AsyncSession,
)

from src.core.settings import load_settings, Settings
from src.database.models import Base

def async_engine() -> AsyncEngine:
    return create_async_engine(load_settings().db_url)


def create_session_factory(engine: Optional[AsyncEngine] = None) -> async_sessionmaker[AsyncSession]:
    
    if engine is None:
        engine = async_engine()
    
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


def async_session(session_factory: Optional[async_sessionmaker[AsyncSession]] = None) -> AsyncSession:
    if session_factory is None:
        session_factory = create_session_factory()
    return session_factory()

# def pg_dump(
#         db_name: str = 'avtoria', 
#         db_user: str = 'postgres', 
#         container_name: str = 'db', 
#         output_path: Optional[str] = None
# ) -> None:

#     if output_path is None:
#         output_path = Settings.path(
#             'src', 'database', 'dumps', datetime.now().strftime("%Y_%m_%d__%H_%M") + '.sql'
#         )

#     subprocess.run([
#         # 'docker',
#         # 'exec', 
#         # '-it', 
#         # container_name, 
#         'pg_dump',
#         '-U', 
#         db_user, 
#         '-d', 
#         db_name,
#         '-a',
#         '-f',
#         output_path
#     ])


async def pg_dump(engine: Optional[AsyncEngine] = None, output_path: Optional[str] = None) -> None:

    timezone = pytz.timezone('Europe/Kyiv')

    if output_path is None:
        output_path = Settings.path(
            'src', 'database', 'dumps', datetime.now(timezone).strftime("%Y_%m_%d__%H_%M") + '.sql'
        )

    if engine is None:
        engine = async_engine()

    metadata = Base.metadata
    
    async with engine.begin() as conn:
        with open(output_path, 'a', encoding='utf-8') as file:
            for table in metadata.sorted_tables:
                set_tablename = True
                result = await conn.execute(table.select())
                for row in result:
                    if set_tablename:
                        file.write(table.name + '\n')
                        set_tablename = False
                    file.write(str(row._asdict()) + '\n')

