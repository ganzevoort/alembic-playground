from pydantic import BaseModel
import uuid


class PortalBase(BaseModel):
    name: str


class PortalCreate(PortalBase):
    pass


class PortalUpdate(PortalBase):
    pass


class PortalResponse(PortalBase):
    id: uuid.UUID

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    portal_id: uuid.UUID


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
