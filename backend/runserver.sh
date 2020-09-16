#! /usr/bin/env bash

# Start the App Server
uvicorn app.main:app --reload --host=0.0.0.0
