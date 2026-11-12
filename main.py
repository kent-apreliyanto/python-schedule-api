import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

conn = sqlite3.connect("schedule.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT NOT NULL,
    activity TEXT
)               
""")
conn.commit()

class Schedule(BaseModel):
    time: str
    activity: str

@app.get("/")
def read_root():
    return {"message": "Welcome to schedule API!"}

@app.get("/schedules")
def get_all_schedules():
    cursor.execute("SELECT * FROM schedules")
    rows = cursor.fetchall()
    
    formatted_data = [{"id": row[0], "time": row[1], "activity": row[2]} for row in rows]
    
    return {"status": "success", "data": formatted_data}

@app.post("/schedules")
def create_schedule(new_item: Schedule):
    cursor.execute(
        "INSERT INTO schedules (time, activity) VALUES (?,?)",
        (new_item.time, new_item.activity)
    )    
    conn.commit()
    return {"status": "success", "message": "schedule added"}

@app.delete("/schedule/{schedule_id}")
def delete_schedule(schedule_id: int):
    cursor.execute(
        "DELETE FROM schedules WHERE id = ?", (schedule_id,)
    )
    conn.commit()
    return {"status": "success", "message": f"Schedule with ID {schedule_id} successfully deleted."}

@app.put("/schedules/{schedule_id}")
def update_schedule(schedule_id: int, update_item: Schedule):
    cursor.execute(
        "UPDATE schedules SET time = ?, activity = ? WHERE id = ?",
        (update_item.time, update_item.activity, schedule_id)
    )
    conn.commit()
    
    if cursor.rowcount == 0:
        return {"status": "failed", "message": f"Schedule with ID {schedule_id} not found."}
    return {"status": "success", "message": f"Schedule with ID {schedule_id} successfully updated."}