from pydantic import BaseModel, Field


class Record(BaseModel):
    room_id: str = Field(...)
    room_name: str = Field(...)
    type: str
