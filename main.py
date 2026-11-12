import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from database import conn, cursor
from models import Schedule

load_dotenv()
app = FastAPI()
SECRET_KEY = os.getenv("API_SECRET_KEY")

def verify_key(x_api_key: str = Header(None)):
    if x_api_key != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Access denied! API Key is incorrect or missing.")

@app.get("/")
def read_root():
    return {"message": "Welcome to schedule API!"}

@app.get("/schedules")
def get_all_schedules():
    cursor.execute("SELECT * FROM schedules")
    rows = cursor.fetchall()
    
    formatted_data = [{"id": row[0], "time": row[1], "activity": row[2]} for row in rows]
    
    return {"status": "success", "data": formatted_data}

@app.post("/schedules", dependencies=[Depends(verify_key)])
def create_schedule(new_item: Schedule):
    cursor.execute(
        "INSERT INTO schedules (time, activity) VALUES (?,?)",
        (new_item.time, new_item.activity)
    )    
    conn.commit()
    return {"status": "success", "message": "schedule added"}

@app.delete("/schedule/{schedule_id}", dependencies=[Depends(verify_key)])
def delete_schedule(schedule_id: int):
    cursor.execute(
        "DELETE FROM schedules WHERE id = ?", (schedule_id,)
    )
    conn.commit()
    return {"status": "success", "message": f"Schedule with ID {schedule_id} successfully deleted."}

@app.put("/schedules/{schedule_id}", dependencies=[Depends(verify_key)])
def update_schedule(schedule_id: int, update_item: Schedule):
    cursor.execute(
        "UPDATE schedules SET time = ?, activity = ? WHERE id = ?",
        (update_item.time, update_item.activity, schedule_id)
    )
    conn.commit()
    
    if cursor.rowcount == 0:
        return {"status": "failed", "message": f"Schedule with ID {schedule_id} not found."}
    return {"status": "success", "message": f"Schedule with ID {schedule_id} successfully updated."}