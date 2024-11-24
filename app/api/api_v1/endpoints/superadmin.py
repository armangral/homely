from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_current_active_super_admin,

    get_session,
)

from app.crud.property import get_active_listings_count, get_insufficient_data_listings_count, get_updated_listings_count
from app.crud.user import (
    create_user_with_admin,
    get_all_users,
    get_all_users_count,
    get_user_by_id,
    get_user_by_username,
    get_users_logged_in_last_24_hours,
    get_users_logged_in_last_n_days,
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


# Get all users count
@router.get("/users/count")
async def fetch_all_users_count(
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    count = await get_all_users_count(db)
    return {"all_users_count": count}


# Get number of users logged in within the last 24 hours
@router.get("/users/logged_in_last_24_hours")
async def fetch_users_logged_in_last_24_hours(
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    count = await get_users_logged_in_last_24_hours(db)
    return {"users_logged_in_last_24_hours": count}


@router.get("/users/logged_in_last_7_days")
async def fetch_users_logged_in_last_7_days(
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    """
    Route to get the number of users logged in within the last 7 days.
    """
    count = await get_users_logged_in_last_n_days(db, days=7)
    return {"users_logged_in_last_7_days": count}


@router.get("/users/logged_in_last_28_days")
async def fetch_users_logged_in_last_28_days(
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    """
    Route to get the number of users logged in within the last 28 days.
    """
    count = await get_users_logged_in_last_n_days(db, days=28)
    return {"users_logged_in_last_28_days": count}


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


@router.get("/properties/active_count")
async def fetch_active_listings_count(
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    """
    Route to get the count of active property listings.
    """
    count = await get_active_listings_count(db)
    return {"active_listings_count": count}


@router.get("/properties/insufficient_data_count")
async def fetch_insufficient_data_listings_count(
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    """
    Route to get the count of listings with insufficient data.
    """
    count = await get_insufficient_data_listings_count(db)
    return {"insufficient_data_listings_count": count}


@router.get("/properties/updated_count")
async def fetch_updated_listings_count(
    db: AsyncSession = Depends(get_session),
    admin=Depends(get_current_active_super_admin),
):
    """
    Route to get the count of property listings updated in the last `days` days.
    """
    count = await get_updated_listings_count(db)
    return {"updated_listings_count": count}


