# Popcorn Prophet

## Large Data Files
This project requires large data files that are not included in the repository due to size constraints. You will need to obtain the following files separately:

- `backend/movies.db`
- `data-analysis/movies.csv`

To get these files, please reach out to me at melissajrichardson99@gmail.com
Once obtained, place each file in its respective directory before running the project.

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
