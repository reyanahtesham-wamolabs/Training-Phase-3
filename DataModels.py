from pydantic import BaseModel,Field,field_validator,model_validator
import uuid
from datetime import datetime,timezone
from enum import Enum



class JobType(str, Enum):
    EMAIL            = "EMAIL"
    REPORT_GENERATION = "REPORT_GENERATION"
    FILE_PROCESSING  = "FILE_PROCESSING"


class inputJob(BaseModel):
    Name:str="Name"
    Priority:int = Field(gt=0,lt=6)
    Type:JobType
class Job (BaseModel):
    ID: str = Field(default_factory=lambda: uuid.uuid4())    
    Name: str
    Type:JobType
    Priority: int
    Status:str="Pending"
    Timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

