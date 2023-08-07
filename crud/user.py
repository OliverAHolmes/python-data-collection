from sqlmodel import Session, select
import db_internal
from models import User


def get_all_users():
    with Session(db_internal.engine) as session:
        statement = select(User)
        results = session.execute(statement)
        return list(i[0] for i in results.all())


def delete_user_by_id(user_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(User, user_id)
        if not row:
            return None
        session.delete(row)
        session.commit()
        return row


def create_new_user(user: User):
    with Session(db_internal.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
