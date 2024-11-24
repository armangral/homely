from typing import Any
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.clients import Client
from app.schemas.clients import ClientCreate, ClientUpdate


# Add a new client
async def add_client(
    db: AsyncSession, client_in: ClientCreate, added_by_id: uuid.UUID
) -> Client:
    new_client = Client(
        client_name=client_in.client_name,
        date_added=client_in.date_added,
        number_of_properties=client_in.number_of_properties,
        average_property_value=client_in.average_property_value,
        status=client_in.status,
        added_by_id=added_by_id,
    )
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client


# Edit client details
async def edit_client(
    db: AsyncSession, client_id: uuid.UUID, client_update: ClientUpdate
) -> Client | None:
    query = select(Client).where(Client.id == client_id)
    result = await db.execute(query)
    client = result.scalar_one_or_none()

    if client:
        for field, value in client_update.dict(exclude_unset=True).items():
            setattr(client, field, value)
        await db.commit()
        await db.refresh(client)
    return client

# Get client by ID
async def get_client_by_id(db: AsyncSession, client_id: uuid.UUID) -> Any:
    query = select(Client).where(Client.id == client_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()



# Set client status
async def set_client_status(
    db: AsyncSession, client_id: uuid.UUID, status: bool
) -> Client | None:
    query = select(Client).where(Client.id == client_id)
    result = await db.execute(query)
    client = result.scalar_one_or_none()

    if client:
        client.status = status
        await db.commit()
        await db.refresh(client)
    return client
