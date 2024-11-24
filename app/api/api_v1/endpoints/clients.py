import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_session, get_current_user
from app.crud.clients import add_client, edit_client, get_client_by_id, set_client_status
from app.schemas.clients import ClientCreate, ClientUpdate, ClientOut

router = APIRouter()


# Add a new client
@router.post("/clients", response_model=ClientOut)
async def create_client(
    client_in: ClientCreate,
    db: AsyncSession = Depends(get_session),
    realtor=Depends(get_current_user)
):
    """
    Create a new client.
    """
    new_client = await add_client(db, client_in, added_by_id=realtor.id)
    return new_client


# Edit an existing client
@router.put("/clients/{client_id}", response_model=ClientOut)
async def update_client(
    client_id: uuid.UUID,
    client_update: ClientUpdate,
    db: AsyncSession = Depends(get_session),
    realtor=Depends(get_current_user),
):
    """
    Edit client details.
    """
    client = await edit_client(db, client_id, client_update)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# get client by id
@router.get("/clients/{client_id}", response_model=ClientOut)
async def get_client(
    client_id: uuid.UUID,
    db: AsyncSession = Depends(get_session),
    realtor=Depends(get_current_user),
):
    """
    Get client by id.
    """
    client = await get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client



# Set client status
@router.patch("/clients/{client_id}/status", response_model=ClientOut)
async def update_client_status(
    client_id: uuid.UUID,
    status: bool,
    db: AsyncSession = Depends(get_session),
    realtor=Depends(get_current_user),
):
    """
    Set client status to active/inactive.
    """
    client = await set_client_status(db, client_id, status)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
