from datetime import datetime
from sqlalchemy import String, Date, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base
from app.models.mixin import SharedMixin


class Client(Base, SharedMixin):
    __tablename__ = "clients"

    # Basic fields
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_added: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)
    number_of_properties: Mapped[int] = mapped_column(Integer, default=0)
    average_property_value: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationship to user (added by)
    added_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    added_by: Mapped["User"] = relationship("User", back_populates="clients")
