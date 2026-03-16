---
name: status
description: Check status of a running job or system overview
---

# /status Skill

You are executing the /status skill.

## Safety
- Read-only — do not modify any files or state

## Execution Contract

1. If a job_id is provided, read the job log and return its current status
2. If no job_id, return a system overview:
   - Total sources in library
   - Recent ingestions (last 7 days)
   - Pending jobs in queue
   - Last heartbeat time
3. Format for Telegram with clean bullet points
