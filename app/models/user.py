from datetime import datetime
from sqlalchemy import Boolean, Date, DateTime, String, Integer, LargeBinary, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from enum import Enum as PEnum

from app.models.mixin import SharedMixin



class User(Base,SharedMixin):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[LargeBinary] = mapped_column(LargeBinary)
    password_salt: Mapped[LargeBinary] = mapped_column(LargeBinary)
    is_super_admin: Mapped[bool] = mapped_column(Boolean)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    clients: Mapped[list["Client"]] = relationship("Client", back_populates="added_by")
