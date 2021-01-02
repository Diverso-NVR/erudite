from pydantic import BaseModel, Field


class Record(BaseModel):
    id: str = Field(None)

    room_id: str = Field(...)
    room_name: str = Field(...)
    date: str = Field(..., description="Date of record", example="2020-09-01")
    start_time: str = Field(..., description="Start time of record", example="13:00")
    end_time: str = Field(..., description="End time of record", example="13:30")

    url: str = Field(None, description="Record url")
    emotions_url: str = Field(None, description="Emotions graph for record")
