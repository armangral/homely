from datetime import date
import uuid
from pydantic import BaseModel


class ClientBase(BaseModel):
    client_name: str
    date_added: date | None = None
    number_of_properties: int = 0
    average_property_value: float | None = None
    status: bool = True


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    client_name: str | None = None
    number_of_properties: int | None = None
    average_property_value: float | None = None
    status: bool | None = None


class ClientOut(ClientBase):
    id: uuid.UUID
    added_by_id: uuid.UUID

    class Config:
        orm_mode = True
