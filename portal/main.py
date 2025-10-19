from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import get_db, engine
from .models import Portal, User, Base
from .schemas import (
    PortalCreate,
    PortalResponse,
    PortalUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Portal Management Service", version="1.0.0")


@app.get("/")
async def root():
    return {"message": "Portal Management Service"}


# Portal endpoints
@app.post("/portals/", response_model=PortalResponse)
async def create_portal(
    portal: PortalCreate,
    db: Session = Depends(get_db),
):
    db_portal = Portal(name=portal.name)
    db.add(db_portal)
    db.commit()
    db.refresh(db_portal)
    return db_portal


@app.get("/portals/", response_model=List[PortalResponse])
async def read_portals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    portals = db.query(Portal).offset(skip).limit(limit).all()
    return portals


@app.get("/portals/{portal_id}", response_model=PortalResponse)
async def read_portal(
    portal_id: str,
    db: Session = Depends(get_db),
):
    portal = db.query(Portal).filter(Portal.id == portal_id).first()
    if portal is None:
        raise HTTPException(status_code=404, detail="Portal not found")
    return portal


@app.put("/portals/{portal_id}", response_model=PortalResponse)
async def update_portal(
    portal_id: str,
    portal: PortalUpdate,
    db: Session = Depends(get_db),
):
    db_portal = db.query(Portal).filter(Portal.id == portal_id).first()
    if db_portal is None:
        raise HTTPException(status_code=404, detail="Portal not found")

    db_portal.name = portal.name
    db.commit()
    db.refresh(db_portal)
    return db_portal


@app.delete("/portals/{portal_id}")
async def delete_portal(
    portal_id: str,
    db: Session = Depends(get_db),
):
    portal = db.query(Portal).filter(Portal.id == portal_id).first()
    if portal is None:
        raise HTTPException(status_code=404, detail="Portal not found")
    db.delete(portal)
    db.commit()
    return {"message": "Portal deleted successfully"}


# User endpoints
@app.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    # Check if portal exists
    portal = db.query(Portal).filter(Portal.id == user.portal_id).first()
    if portal is None:
        raise HTTPException(status_code=404, detail="Portal not found")

    db_user = User(name=user.name, portal_id=user.portal_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/portals/{portal_id}/users/", response_model=List[UserResponse])
async def read_portal_users(
    portal_id: str,
    db: Session = Depends(get_db),
):
    # Check if portal exists
    portal = db.query(Portal).filter(Portal.id == portal_id).first()
    if portal is None:
        raise HTTPException(status_code=404, detail="Portal not found")

    users = db.query(User).filter(User.portal_id == portal_id).all()
    return users


@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user: UserUpdate,
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if new portal exists
    portal = db.query(Portal).filter(Portal.id == user.portal_id).first()
    if portal is None:
        raise HTTPException(status_code=404, detail="Portal not found")

    db_user.name = user.name
    db_user.portal_id = user.portal_id
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
