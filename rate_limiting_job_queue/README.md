# Concurrent Job Queue API (FastAPI)

A backend system built using **FastAPI** that manages background jobs with **per-user concurrency limits**, **FIFO queuing**, and **thread-safe execution**.

This project demonstrates core backend concepts like:
- Concurrency
- Threading
- Locks & race-condition handling
- Job scheduling
- Logging
- System design fundamentals

---

## 🚀 Features

- ✅ Submit background jobs via API
- ✅ Maximum **2 concurrent jobs per user**
- ✅ Extra jobs are queued (FIFO per user)
- ✅ Automatic job promotion when a running job completes
- ✅ Thread-safe shared state using locks
- ✅ Centralized logging (file + console)
- ✅ Job status tracking APIs

---

## 🧠 High-Level Design

- **ThreadPoolExecutor** executes jobs concurrently
- **Per-user running count** enforces concurrency limit
- **Per-user queue (deque)** stores waiting jobs
- **Lock (`threading.Lock`)** prevents race conditions
- **Job lifecycle states**:
  - `SUBMITTED`
  - `QUEUED`
  - `RUNNING`
  - `COMPLETED`

---

## ⚙️ Tech Stack

- Python
- FastAPI
- ThreadPoolExecutor
- threading
- logging

---

## 📌 Job Lifecycle

1. User submits a job
2. If user has < 2 running jobs → job starts immediately
3. Else → job is added to user queue
4. When a job completes:
   - Running count decreases
   - Next queued job (if any) is promoted

---

## 🧪 API Endpoints

### ➤ Submit a Job
POST /jobs?user_id=<user>&payload=<data>
Response:
```json
{
  "job_id": "uuid",
  "status": "RUNNING | QUEUED"
}
```
### ➤ Get Job Status
GET /jobs/{job_id}

### ➤ Get All jobs for a User
GET /users/{user_id}/jobs

---

## 🧵 Concurrency & Safety

- Shared structures protected by locks:
- - jobs_submitted
- - user_running_count
- - user_queue
- Prevents race conditions and inconsistent states
- FIFO fairness maintained per user

---

## 📝 Logging

Logs are written to:
- UserAPI.log
- Console output
Log levels used:
- INFO → job lifecycle events
- WARNING → invalid lookups
- ERROR → job execution failures

---

## 📈 Future Improvements

- Persist jobs using Redis / Database
- Support job retries & failures
- Graceful recovery on server restart
- Distributed worker support (Celery / RQ)
- Metrics & monitoring

---

## 👨‍💻 Author

**Milli Srivastava**

Backend & Systems Enthusiast

⭐ If you find this useful, feel free to star the repository!
