from fastapi import APIRouter, Depends, status
from schemas.column_constraint import ConstraintRead, ConstraintUpdate
from db_internal import SessionLocal
from sqlalchemy.orm import Session

from sqlmodel import Session
from crud.column_constraint import (
    get_constraint,
    update_constraint,
    list_constraints,
)

router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{constraint_id}", response_model=ConstraintRead)
def read_constraint_route(constraint_id: int, db: Session = Depends(get_db)):
    constraint = get_constraint(db, constraint_id)
    if not constraint:
        raise HTTPException(status_code=404, detail="Constraint not found")
    return constraint


@router.put("/{constraint_id}", response_model=ConstraintRead)
def update_constraint_route(
    constraint_id: int, constraint_data: ConstraintUpdate, db: Session = Depends(get_db)
):
    constraint = get_constraint(db, constraint_id)
    if not constraint:
        raise HTTPException(status_code=404, detail="Constraint not found")
    updated_constraint = update_constraint(db, constraint_id, constraint_data)
    return updated_constraint


@router.get("/", response_model=list[ConstraintRead])
def list_constraints_route(db: Session = Depends(get_db)):
    constraints = list_constraints(db)
    return constraints
