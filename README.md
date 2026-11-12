# Daily Schedule REST API

A modern, lightweight backend microservice built with python and FastAPI to manage daily activity schedules.

## Features
- **GET /schedules**: Fetch all schedules
- **POST /schedules**: Create a new schedule
- **DELETE /schedules/{id}**: Delete a specific schedule

## Technology Stack
- Python 3
- FastAPI
- Uvicorn (ASGI Server)

## How to Run
1. Create a virtual environment: `python -m venv env`
2. Activate the environment: `.\env\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start the server: `uvicorn main:pp --reload`