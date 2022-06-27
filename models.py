from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel


class Hero (BaseModel):
    id: Optional[UUID] = uuid4()
    name: str
