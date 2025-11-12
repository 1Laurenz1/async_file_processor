from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.file_entity import FileEntity


class FileEntity(ABC):
    @abstractmethod
    async def save(self, file_entityt: FileEntity) -> None:
        pass
    
    
    @abstractmethod
    async def get_by_id(self, file_id: str) -> Optional[FileEntity]:
        pass
    
    
    @abstractmethod
    async def get_all(self) -> List[FileEntity]:
        pass