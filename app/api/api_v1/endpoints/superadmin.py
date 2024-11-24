from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_active_super_admin,

    get_session,
)

from app.crud.user import (
    create_user_with_admin,
    get_all_users,
    get_user_by_id,
    get_user_by_username,
)


from app.schemas.user import UserCreateWithAdmin, UserOut

router = APIRouter()




# Get all users
@router.get("/users", response_model=list[UserOut])
async def fetch_all_users(
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    users = await get_all_users(db)
    if not users:
        return []
    return users


@router.post("/users")
async def create_new_user(
    user_in: UserCreateWithAdmin,
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    user = await get_user_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    await create_user_with_admin(db, user_in)

    await db.commit()
    return {"msg": "User created successfully"}

# Set the status of user as active
@router.put("/users/{user_id}")
async def activate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    await db.commit()
    return {"msg": "User activated successfully"}

# Set the status of user as inactive
@router.delete("/users/{user_id}")
async def deactivate_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    await db.commit()
    return {"msg": "User deactivated successfully"}
