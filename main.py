from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Schedule(BaseModel):
    time: str
    activity: str
    
daily_schedule = [
    {"id": 1, "time": "08.00", "activity": "Prepare Python portofolio"},
    {"id": 2, "time": "09.00", "activity": "Launch break"},
]

@app.get("/")
def read_root():
    return {"message": "Welcome to schedule API!"}

@app.get("/schedules")
def get_all_schedules():
    return {"status": "success", "data": daily_schedule}

@app.post("/schedules")
def create_schedule(new_item: Schedule):
    new_id = len(daily_schedule) + 1
    
    new_data = {
        "id": new_id,
        "time": new_item.time,
        "activity": new_item.activity
    }
    
    daily_schedule.append(new_data)
    
    return {"status": "success", "message": "schedule added", "data": new_data}

@app.delete("/schedule/{schedule_id}")
def delete_schedule(schedule_id: int):
    for i, schedule in enumerate(daily_schedule):
        if schedule["id"] == schedule_id:
            del daily_schedule[i]
            return {"status": "success", "message": f"Schedule with ID {schedule_id} successfully deleted."}
    return {"status": "error", "message": f"Schedule with ID {schedule_id} not found."}