#!/bin/bash
# Script to run the FastAPI backend server

cd "$(dirname "$0")"
uvicorn main:app --reload --port 8000
