"""
Database models and schemas
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============ Enums ============

class ProjectStatus(str, Enum):
    """Project status states"""
    OFFLINE = "offline"
    RUNNING = "running"
    STARTING = "starting"
    STOPPING = "stopping"
    ERROR = "error"
    PAUSED = "paused"


class ProjectType(str, Enum):
    """Supported project types"""
    PYTHON_BOT = "python_bot"
    NODEJS = "nodejs"
    NODEJS_BOT = "nodejs_bot"
    FILE = "file"
    ZIP = "zip"


# ============ User Models ============

class UserCreate(BaseModel):
    """User creation schema"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    language: str = "en"


class UserUpdate(BaseModel):
    """User update schema"""
    username: Optional[str] = None
    language: Optional[str] = None
    storage_limit: Optional[int] = None


class User(UserCreate):
    """User model"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    storage_used: int = 0
    storage_limit: int = 5 * 1024 * 1024 * 1024  # 5GB
    is_premium: bool = False
    is_banned: bool = False
    projects_count: int = 0
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": 123456789,
                "username": "john_doe",
                "first_name": "John",
                "language": "en",
                "storage_used": 1024000,
                "storage_limit": 5368709120,
                "is_premium": False,
            }
        }


# ============ File Models ============

class FileCreate(BaseModel):
    """File creation schema"""
    filename: str
    size: int
    mime_type: str
    project_id: Optional[str] = None


class FileUpdate(BaseModel):
    """File update schema"""
    filename: Optional[str] = None
    is_public: Optional[bool] = None


class File(FileCreate):
    """File model"""
    file_id: str
    user_id: int
    path: str
    url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    downloads: int = 0
    is_public: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "file_id": "file_abc123",
                "user_id": 123456789,
                "filename": "bot.zip",
                "size": 1024000,
                "mime_type": "application/zip",
                "path": "/storage/files/bot.zip",
            }
        }


# ============ Log Models ============

class LogCreate(BaseModel):
    """Log creation schema"""
    project_id: str
    level: str  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LogEntry(LogCreate):
    """Log entry model"""
    log_id: str
    
    class Config:
        schema_extra = {
            "example": {
                "log_id": "log_xyz789",
                "project_id": "proj_abc123",
                "level": "INFO",
                "message": "Bot started successfully",
                "timestamp": "2026-05-19T18:30:00",
            }
        }


# ============ Project Models ============

class ProjectStats(BaseModel):
    """Project statistics"""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    uptime_seconds: int = 0
    restarts: int = 0
    last_error: Optional[str] = None
    last_error_time: Optional[datetime] = None


class ProjectCreate(BaseModel):
    """Project creation schema"""
    name: str
    project_type: ProjectType
    description: Optional[str] = None
    startup_command: Optional[str] = None


class ProjectUpdate(BaseModel):
    """Project update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    startup_command: Optional[str] = None
    status: Optional[ProjectStatus] = None


class Project(ProjectCreate):
    """Project model"""
    project_id: str
    user_id: int
    status: ProjectStatus = ProjectStatus.OFFLINE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    files: List[str] = []  # File IDs
    logs: List[str] = []  # Log IDs
    stats: ProjectStats = Field(default_factory=ProjectStats)
    environment: Dict[str, str] = {}
    requirements: Dict[str, str] = {}  # Detected dependencies
    size_mb: float = 0.0
    is_public: bool = False
    
    class Config:
        schema_extra = {
            "example": {
                "project_id": "proj_abc123",
                "user_id": 123456789,
                "name": "Anime Bot",
                "project_type": "python_bot",
                "description": "My awesome anime bot",
                "status": "running",
                "size_mb": 15.5,
                "stats": {
                    "cpu_percent": 5.2,
                    "memory_mb": 128.4,
                    "uptime_seconds": 3600,
                }
            }
        }


# ============ System Models ============

class SystemStats(BaseModel):
    """System statistics"""
    total_users: int = 0
    active_projects: int = 0
    total_projects: int = 0
    storage_used_gb: float = 0.0
    storage_limit_gb: float = 100.0
    uptime_seconds: int = 0
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    
    class Config:
        schema_extra = {
            "example": {
                "total_users": 150,
                "active_projects": 45,
                "total_projects": 230,
                "storage_used_gb": 45.5,
                "cpu_percent": 35.2,
                "memory_percent": 62.1,
            }
        }


# ============ API Response Models ============

class APIResponse(BaseModel):
    """Standard API response"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Operation successful",
                "data": {"project_id": "proj_abc123"},
                "timestamp": "2026-05-19T18:30:00",
            }
        }


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    code: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "Project not found",
                "code": "PROJECT_NOT_FOUND",
                "timestamp": "2026-05-19T18:30:00",
            }
        }
