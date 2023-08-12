#!/bin/bash

alembic upgrade head

gunicorn -w 16 -k uvicorn.workers.UvicornWorker main:app --bind=0.0.0.0:8000 --reload