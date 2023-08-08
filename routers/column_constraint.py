from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlmodel import Session
from schemas.column_constraint import ConstraintRead, ConstraintUpdate
from crud.column_constraint import (
    get_constraint,
    update_constraint,
    list_constraints,
)
from db_internal import get_db
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{constraint_id}", response_model=ConstraintRead)
async def read_constraint_route(constraint_id: int, db: Session = Depends(get_db)):
    constraint = get_constraint(db, constraint_id)
    if not constraint:
        raise HTTPException(status_code=404, detail="Constraint not found")
    return constraint


@router.put("/{constraint_id}", response_model=ConstraintRead)
async def update_constraint_route(
    constraint_id: int, constraint_data: ConstraintUpdate, db: Session = Depends(get_db)
):
    return update_constraint(db, constraint_id, constraint_data)


@router.get("/", response_model=list[ConstraintRead])
async def list_constraints_route(db: Session = Depends(get_db)):
    constraints = list_constraints(db)
    return constraints
