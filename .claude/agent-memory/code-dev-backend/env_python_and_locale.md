---
name: env-python-and-locale
description: This Windows dev box has no python/pytest on PATH — use the Anaconda interpreter; also Windows GBK locale breaks non-ASCII .ini config files
metadata:
  type: reference
---

Two non-obvious environment facts for backend work in this repo (`C:\develop\aiws\money`):

1. **No Python on PATH.** `python`, `python3`, `py`, and `pip` are all missing/are Store
   stubs. The working interpreter is **Anaconda**:
   `C:\Users\houjinxin\anaconda3\python.exe` (Python 3.14 as of 2026-08-08).
   - Run tests: `cd backend && C:/Users/houjinxin/anaconda3/python.exe -m pytest tests/ -q`
   - Run alembic: `... python.exe -m alembic upgrade head`
   - This env ships sqlalchemy/pydantic/httpx/pytest but was MISSING fastapi/pymysql/alembic
     — had to `python -m pip install fastapi pymysql alembic` (and `python-jose`/`passlib` for TASK02).
   - Always verify the interpreter still exists before relying on it.

2. **Windows locale is GBK (cp936).** Python's `configparser` reads `.ini` files with
   `encoding="locale"`, so any non-ASCII bytes (Chinese comments) in `alembic.ini` /
   `pytest.ini` / `.cfg` crash with `UnicodeDecodeError: 'gbk' codec`. **Keep all
   `.ini`/config files ASCII-only** in this repo (the skeleton `alembic.ini` had Chinese
   comments and had to be rewritten to ASCII). Code files (.py) are fine with UTF-8.

How to apply: when running backend tooling here, use the full Anaconda path; when creating
any `.ini`/`.cfg` config, use English-only comments. Related: [[code-agent-framework]].
