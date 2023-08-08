from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.column_constraint import ConstraintUpdate
from models import ColumnConstraint


# Get a constraint by its ID
def get_constraint(db: Session, constraint_id: int) -> Optional[ColumnConstraint]:
    return (
        db.query(ColumnConstraint).filter(ColumnConstraint.id == constraint_id).first()
    )


# Update a constraint
def update_constraint(
    db: Session, constraint_id: int, constraint_data: ConstraintUpdate
) -> ColumnConstraint:
    existing_constraint = db.get(ColumnConstraint, constraint_id)
    if not existing_constraint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Constraint not found",
        )
    # Update the fields of the existing table configuration
    for key, value in constraint_data.dict(exclude_unset=True).items():
        setattr(existing_constraint, key, value)

    db.add(existing_constraint)
    db.commit()
    db.refresh(existing_constraint)

    return existing_constraint


# List all constraints
def list_constraints(db: Session) -> List[ColumnConstraint]:
    return db.query(ColumnConstraint).all()
