from dataclasses import dataclass

from datetime import datetime

from app.domain.value.file_status import FileStatus


@dataclass(frozen=True, slots=True)
class FileEntity:
    id: str
    original_name: str
    file_path: str
    file_size: int
    mime_type: str
    status:  FileStatus
    created_at: datetime
    
    
    def can_be_processed(self) -> bool:
        return self.status == FileStatus.PENDING
    
    
    def is_too_large(self, max_size_mb: int = 100) -> bool:
        return self.file_size > max_size_mb * 1024 * 1024
    
    
    def get_extension(self) -> str:
        return self.original_name.split('.')[-1].lower() if '.' in self.original_name else ""


    def mark_completed(self) -> None:
        if self.status != FileStatus.PROCESSING:
            raise ValueError(f"File {self.id} cannot be completed from {self.status}")
        self.status = FileStatus.COMPLETED
        
        
    def mark_failed(self, reason: str = "") -> None:
        self.status = FileStatus.FAILED
    
    
    def mark_processing(self) -> None:
        if not self.can_be_processed():
            raise ValueError(f"File {self.id} cannot be processed")
        self.status = FileStatus.PROCESSING