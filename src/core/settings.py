from pydantic_settings import BaseSettings, SettingsConfigDict

import os
from functools import lru_cache
from typing import (
    Optional, 
    Union, 
    Dict, 
    Any,
    TypeAlias,
    Union,
    List,
)
from pathlib import Path


_StrPath: TypeAlias = Union[os.PathLike[str], str, Path]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file='./.env', 
        env_file_encoding='utf-8', 
        case_sensitive=False
    )
  
    database_uri: str
    database_name: str
    database_host: Optional[str] = None
    database_port: Optional[int] = None
    database_user: Optional[str] = None
    database_password: Optional[str] = None
    

    @property
    def db_url(self) -> str:
        
        return self.database_uri.format(
            self.database_user,
            self.database_password,
            self.database_host,
            self.database_port,
            self.database_name,
        )

    @staticmethod
    def root_dir() -> Path:
        return Path(__file__).resolve().parent.parent.parent
    
    @classmethod
    def path(cls, *paths: _StrPath, base_path: Optional[_StrPath] = None) -> str:

        if base_path is None:
            base_path = cls.root_dir()
        
        return os.path.join(base_path, *paths)


@lru_cache(typed=True)
def load_settings() -> Settings: 
    return Settings() # type: ignore