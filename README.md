# Kala python client

Kala is a simplistic, modern, and performant job scheduler written in Go. It lives in a single binary and does not have any dependencies.

# Getting Started

```python
from kala import Client
cl = Client("http://127.0.0.1:8000")

cl.list_jobs()
```

## Create new job

```python
from kala.models import Job

data = {
    "epsilon": "PT5S",
    "command": "bash /home/ajvb/gocode/src/github.com/ajvb/kala/examples/example-kala-commands/example-command.sh",
    "name": "test_job",
    "schedule": "R2/2017-06-04T19:25:16.828696-07:00/PT10S"}

job = Job(**data)
jid = cl.create_job(job)
```
