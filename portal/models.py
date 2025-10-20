from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid


Base = declarative_base()


class Portal(Base):
    __tablename__ = "portals"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    logo = Column(String)
    name = Column(
        String,
        nullable=False,
    )

    # Relationship
    users = relationship("User", back_populates="portal")


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = Column(
        String,
        nullable=False,
    )
    email = Column(
        String,
        nullable=True,
    )
    portal_id = Column(
        UUID(as_uuid=True),
        ForeignKey("portals.id"),
        nullable=False,
    )

    # Relationship
    portal = relationship("Portal", back_populates="users")
