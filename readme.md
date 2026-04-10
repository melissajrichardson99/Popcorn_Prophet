# Popcorn Prophet

## Prerequisites
- Frontend: [Bun v1.3.2](https://bun.sh/)
- Backend: [Python 3.13.5](https://www.python.org/downloads/)

## Start Frontend Development Server Locally

```bash
$ cd frontend
$ bun install
$ bun run dev
```

## Start Backend Development Server Locally
```bash
$ cd backend
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ fastapi dev main.py
```