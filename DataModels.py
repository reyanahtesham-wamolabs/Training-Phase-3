from pydantic import BaseModel,Field,field_validator,model_validator
import uuid
from datetime import datetime,timezone
from enum import Enum
from abc import ABC,abstractmethod
import asyncio

runningJobs=[]
class JobType(str, Enum):
    EMAIL            = "EMAIL"
    REPORT_GENERATION = "REPORT_GENERATION"
    FILE_PROCESSING  = "FILE_PROCESSING"


class inputJob(BaseModel):
    Name:str="Name"
    Priority:int = Field(gt=0,lt=6)
    Type:JobType
class Job (BaseModel):
    ID: str = Field(default_factory=lambda: str(uuid.uuid4()))    
    Name: str
    Type:JobType
    Priority: int
    Status:str="Pending"
    Timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobProcessor(ABC):
    @abstractmethod
    async def RunJob(job:Job):
        pass

class EmailJobProcessor(JobProcessor):
    async def RunJob(job:Job):
        job.Status="PROCESSING"
        runningJobs.append([job,"STARTED"])
        for i in range(10):       
            if i==1:
                runningJobs.append([job,"10% COMPLETE"])
            if i==6:
                runningJobs.append([job,"50% COMPLETE"])
            await asyncio.sleep(1)
        runningJobs.append([job,"100% COMPLETED"])
        job.Status="COMPLETED"


class ReportJobProcessor(JobProcessor):
    async def RunJob(job:Job):
        job.Status="PROCESSING"
        runningJobs.append([job,"STARTED"])
        for i in range(15):       
            if i==1:
                runningJobs.append([job,"10% COMPLETE"])
            if i==8:
                runningJobs.append([job,"50% COMPLETE"])
            await asyncio.sleep(1)
        runningJobs.append([job,"100% COMPLETED"])
        job.Status="COMPLETED"

class FileJobProcessor(JobProcessor):
    async def RunJob(job:Job):
        job.Status="PROCESSING"
        runningJobs.append([job,"STARTED"])
        for i in range(20):       
            if i==2:
                runningJobs.append([job,"10% COMPLETE"])
            if i==10:
                runningJobs.append([job,"50% COMPLETE"])
            await asyncio.sleep(1)
        runningJobs.append([job,"100% COMPLETED"])
        job.Status="COMPLETED"

class JobProcessorFactory(JobProcessor):
    _Processor={
        "email":EmailJobProcessor,
        "report":ReportJobProcessor,
        "file":FileJobProcessor
    }
    @classmethod
    def create(cls,name:str):
        
        process=cls._Processor[name.lower()]
        return process 
