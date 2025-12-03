#!/bin/bash
cd /home/site/wwwroot
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app --bind 0.0.0.0:8000
