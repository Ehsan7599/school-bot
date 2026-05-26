from database.db import SessionLocal

from models.registration import Registration

from models.user import User


def get_all_registrations():

    db = SessionLocal()

    registrations = db.query(Registration).all()

    db.close()

    return registrations


def create_registration(
    parent_bale_id,
    student_name,
    grade,
    parent_phone
):

    db = SessionLocal()

    new_registration = Registration(
        parent_bale_id=str(parent_bale_id),
        student_name=student_name,
        grade=grade,
        parent_phone=parent_phone
    )

    db.add(new_registration)

    db.commit()

    db.refresh(new_registration)

    db.close()

    return new_registration


def update_registration_status(
    registration_id,
    new_status
):

    db = SessionLocal()

    registration = db.query(Registration).filter(
        Registration.id == registration_id
    ).first()

    if registration:

        registration.status = new_status

        db.commit()

    db.close()


def is_admin(bale_id):

    db = SessionLocal()

    user = db.query(User).filter(
        User.bale_id == str(bale_id)
    ).first()

    db.close()

    if not user:

        return False

    return user.role == "admin"
def get_registrations_count():

    db = SessionLocal()

    count = db.query(Registration).count()

    db.close()

    return count


def get_accepted_count():

    db = SessionLocal()

    count = db.query(Registration).filter(
        Registration.status == "accepted"
    ).count()

    db.close()

    return count


def get_rejected_count():

    db = SessionLocal()

    count = db.query(Registration).filter(
        Registration.status == "rejected"
    ).count()

    db.close()

    return count


def get_pending_count():

    db = SessionLocal()

    count = db.query(Registration).filter(
        Registration.status == "pending"
    ).count()

    db.close()

    return count
def search_registrations(search_text):

    db = SessionLocal()

    results = db.query(Registration).filter(
        Registration.student_name.contains(search_text)
    ).all()

    db.close()

    return results