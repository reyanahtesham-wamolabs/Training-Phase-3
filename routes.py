# This is the page that contains all the routes
from fastapi import  APIRouter,BackgroundTasks
import asyncio
from DataModels import JobType,Job,inputJob
from services import JobProcessorFactory
from DataJobs import totalJobs,registryJobs
#from app import RunJob


router=APIRouter()

async def RunJob(job:Job):
    process=JobProcessorFactory.create(job.Type.value)
    await process.RunJob(job)

#Route to create a job
@router.post("/CreateJob")
def create_jobs(inputJob:inputJob,background_tasks: BackgroundTasks):
    #input job being used to 
    job=Job(Name=inputJob.Name,Priority=inputJob.Priority,Type=inputJob.Type)
    registryJobs.append(job)
    totalJobs.append(job)
    totalJobs.sort(key=lambda x: x.Priority)
    PriorityJob=totalJobs.pop()
    background_tasks.add_task(RunJob,PriorityJob)
    return job

@router.get("/GetDetails/{name}")
def get_details(name:str):
    foundJobs=[job for job in registryJobs if job.Name==name]       
    if foundJobs:
        return foundJobs
    return "No jobs found"

@router.get("/AllJobs/")
def get_all_jobs(Name:str|None=None,Type:JobType|None=None,Priority:str|None=None,Status:str|None=None,
                 pageNumber:int|None=1,pageSize:int|None=None):
    filteredJob=registryJobs
    if Name:
        filteredJob=[job for job in filteredJob if Name==job.Name]
    if Type:
        filteredJob=[job for job in filteredJob if Type==job.JobType]
    if Priority:
        filteredJob=[job for job in filteredJob if Priority==job.Priority]
    if Status:
        filteredJob=[job for job in filteredJob if Status==job.Status]
    page=filteredJob
    if pageSize:
        page=filteredJob[pageSize*pageNumber-pageSize:pageSize*pageNumber]
    return page

@router.delete("/DeleteJob/{name}")
def delete_job(name:str):
    registryJobs=[job for job in registryJobs if not job.Name==name]
    return registryJobs

@router.get("/Stats")
def getStats():
    StatsObj={"PENDING":0,"PROCESSING":0,"COMPLETED":0,"FAILED":0}
    for job in registryJobs:
        if job.Status=="PROCESSING":
            StatsObj["PROCESSING"]+=1
        if job.Status=="PENDING":
            StatsObj["PENDING"]+=1
        if job.Status=="COMPLETED":
            StatsObj["COMPLETED"]+=1
        if job.Status=="FAILED":
            StatsObj["FAILED"]+=1
    return StatsObj

