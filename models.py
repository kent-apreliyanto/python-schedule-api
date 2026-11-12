from pydantic import BaseModel, Field

class Schedule(BaseModel):
    time: str = Field(..., pattern=r"^(?:[01]\d|2[0-3])[:.][0-5]\d$")
    activity: str