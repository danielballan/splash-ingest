from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class RevisionStamp(BaseModel):
    user: str
    time: datetime
    version_id: str


class JobStatus(str, Enum):
    submitted = 'submitted'
    running = 'running'
    successful = 'successful'
    error = 'error'


class StatusItem(BaseModel):
    time: datetime
    status: JobStatus
    log: Optional[str]
    submitter: str


class Job(BaseModel):
    id: Optional[str] = None
    submit_time: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    document_path: str
    status: JobStatus = None
    mapping_id: Optional[str] = None
    submitter: Optional[str]
    status_history: Optional[List[StatusItem]] = []


class Entity(BaseModel):
    uid: str
    name: str
    org: str
    hashed_pw: str
