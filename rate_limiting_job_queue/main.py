from fastapi import FastAPI
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import uuid
import threading
import time
from collections import defaultdict, deque
import logging

logging.basicConfig(          
    level=logging.INFO,       
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("UserAPI.log"),        
        logging.StreamHandler()                #for terminal
    ]
)

logger = logging.getLogger("user-api")    

app = FastAPI()

class JobStatus(Enum):
    SUBMITTED = "SUBMITTED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"

class Job:
    def __init__(self, job_id, user_id, payload):
        self.job_id = job_id
        self.user_id = user_id
        self.payload = payload
        self.status = JobStatus.SUBMITTED


jobs_submitted = {}
user_running_count = defaultdict(int)
user_queue = defaultdict(deque)

lock = threading.Lock()

def process_job(job):
    try:
        logger.info(f"Started job {job.job_id} for user {job.user_id}")
        time.sleep(5)
    
        with lock:
            job.status = JobStatus.COMPLETED
            logger.info(f"Completed job {job.job_id} for user {job.user_id}")
            user_running_count[job.user_id] -= 1
        promote_job(job.user_id)
    except Exception as e:
        logger.error(f"Job {job.job_id} failed for user {job.user_id}: {e}")
        
executor = ThreadPoolExecutor(max_workers = None)

def promote_job(user_id):
    if user_queue[user_id] and user_running_count[user_id] < 2:
        next_job = user_queue[user_id].popleft()
        next_job.status = JobStatus.RUNNING
        user_running_count[user_id] += 1
        executor.submit(process_job, next_job)
    
    
@app.post("/jobs")
def submit_job(user_id: str, payload: str):
    job_id = str(uuid.uuid4())
    job = Job(job_id, user_id, payload)
    logger.info(f"Job {job_id} submitted for user {user_id}")
    with lock:
        jobs_submitted[job.job_id] = job

        if user_running_count[user_id] < 2:
            job.status = JobStatus.RUNNING
            user_running_count[user_id] += 1
            executor.submit(process_job, job)

        else:
            job.status = JobStatus.QUEUED
            user_queue[user_id].append(job)
    return {
        "job_id": job.job_id,
        "status": job.status.value
    }

@app.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    job = jobs_submitted.get(job_id)
    if not job:
        logger.warning(f"Job not found: {job_id}")
        
    return {
        "job_id": job.job_id,
        "user_id": job.user_id,
        "status": job.status.value
    }

@app.get("/users/{user_id}/jobs")
def get_user_jobs(user_id: str):
    result = []
    for job in jobs_submitted.values():
        if job.user_id == user_id:
            result.append({
                "job_id": job.job_id,
                "status": job.status.value
            })
        else:
            logger.warning(f"No jobs found for user {user_id}")
    return result






