# import models, schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from schemas.column_constraint import ConstraintCreate, ConstraintUpdate
from models import ColumnConstraint


# Create a new constraint
def create_constraint(db: Session, constraint: ConstraintCreate) -> ColumnConstraint:
    db_constraint = ColumnConstraint(**constraint.dict())
    db.add(db_constraint)
    db.commit()
    db.refresh(db_constraint)
    return db_constraint


# Get a constraint by its ID
def get_constraint(db: Session, constraint_id: int) -> Optional[ColumnConstraint]:
    return db.query(ColumnConstraint).filter(ColumnConstraint.id == constraint_id).first()


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


# Delete a constraint
def delete_constraint(db: Session, constraint_id: int) -> bool:
    db_constraint = db.query(ColumnConstraint).filter(ColumnConstraint.id == constraint_id).first()
    if db_constraint:
        db.delete(db_constraint)
        db.commit()
        return True
    return False


# List all constraints (optional)
def list_constraints(db: Session) -> List[ColumnConstraint]:
    return db.query(ColumnConstraint).all()
