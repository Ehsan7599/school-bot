from database.db import SessionLocal
from models.user import User


def get_user_by_bale_id(bale_id):

    db = SessionLocal()

    user = db.query(User).filter(
        User.bale_id == str(bale_id)
    ).first()

    db.close()

    return user


def create_user(bale_id, first_name, username):

    db = SessionLocal()

    new_user = User(
        bale_id=str(bale_id),
        first_name=first_name,
        username=username
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    db.close()

    return new_user
def update_user_role(bale_id, new_role):

    db = SessionLocal()

    user = db.query(User).filter(
        User.bale_id == str(bale_id)
    ).first()

    if user:

        user.role = new_role

        db.commit()

    db.close()

    return user
def update_user_state(bale_id, new_state):

    db = SessionLocal()

    user = db.query(User).filter(
        User.bale_id == str(bale_id)
    ).first()

    if user:

        user.state = new_state

        db.commit()

    db.close()


def get_user_state(bale_id):

    db = SessionLocal()

    user = db.query(User).filter(
        User.bale_id == str(bale_id)
    ).first()

    state = ""

    if user:

        state = user.state

    db.close()

    return state
def is_admin(bale_id):

    db = SessionLocal()

    user = db.query(User).filter(
        User.bale_id == str(bale_id)
    ).first()

    db.close()

    if user and user.role == "admin":

        return True

    return False