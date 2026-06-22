from abc import ABC,abstractmethod
from DataModels import Job
import asyncio
import logging
from DataJobs import runningJobs

class AppLogger:
    _instance = None        # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        logging.basicConfig(filename="newfile.log",
                            format='%(asctime)s %(levelname)s: %(message)s',
                            filemode='w')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)


    def info(self, msg):    self.logger.info(msg)
    def debug(self, msg):   self.logger.debug(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg):   self.logger.error(msg)

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

