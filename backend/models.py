from sqlmodel import SQLModel, Field
from typing import Optional

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ts: float
    src_ip: str
    severity: float
    raw: str
