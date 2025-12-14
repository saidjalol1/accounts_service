from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from services.db_conf import Base, current_time


class Users(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid4,nullable=False,)

    email = Column(String(255),unique=True,index=True,nullable=False)
    password = Column(String(255),nullable=False)

    is_active = Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime(timezone=True),default=current_time,nullable=False)
    updated_at = Column(DateTime(timezone=True),onupdate=current_time)

