from pydantic import BaseModel,Field,field_validator
from fastapi import FastAPI, Depends, APIRouter,BackgroundTasks,Request
import uuid
from datetime import datetime,timezone


App=FastAPI()
router=APIRouter()
totalJobs=[]
class Job (BaseModel):
    ID: str = Field(default_factory=lambda: uuid.uuid4())    
    Name: str
    Type:str
    Priority: int
    Status:str
    Timestamp: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))


@router.post("/CreateJob")
def get_multiple_users(job:Job):
    # fullJob=JobWithIDandTime(job)
    totalJobs.append(job)
    return job

@router.get("/GetDetails/{name}")
def get_multiple_users(name:str):
    foundJobs=[job for job in totalJobs if job.Name==name]
       
    if foundJobs:
        return foundJobs
    return "No jobs found"

@router.get("/AllJobs/")
def getAllJobs(sort:str|None=None,page:int|None=None):
    totalJobs
    return 1

@router.delete("/DeleteJob/{name}")
def deleteJob(name:str):
    totalJobs=[job for job in totalJobs if not job.Name==name]
    return totalJobs

@router.get("/Stats")
def getStats():
    
    return totalJobs
App.include_router(router)
