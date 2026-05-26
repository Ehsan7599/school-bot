from fastapi import APIRouter

from temp_data import registration_data

from services.registration_service import (
    create_registration,
    get_all_registrations,
    update_registration_status,
    is_admin
)

from services.user_service import (
    get_user_by_bale_id,
    create_user,
    update_user_role,
    update_user_state,
    get_user_state
)

from services.ai_service import (
    generate_response,
    send_message
)

router = APIRouter(prefix="/bale")


@router.post("/webhook")
async def bale_webhook(data: dict):

    print("FULL DATA:")
    print(data)

    message = data.get("message", {})

    user_data = message.get("from", {})

    bale_id = user_data.get("id")

    first_name = user_data.get("first_name", "")

    username = user_data.get("username", "")

    chat = message.get("chat", {})
    chat_id = chat.get("id")

    user_text = message.get("text", "")

    existing_user = get_user_by_bale_id(bale_id)

    if not existing_user:

        create_user(
            bale_id=bale_id,
            first_name=first_name,
            username=username
        )

        print("New user saved!")

        user_role = "parent"

    else:

        user_role = existing_user.role

    current_state = get_user_state(bale_id)

    # ---------------- SET ROLE ----------------

    if user_text.startswith("/setrole"):

        parts = user_text.split()

        if len(parts) == 3:

            target_bale_id = parts[1]

            new_role = parts[2]

            update_user_role(
                target_bale_id,
                new_role
            )

            send_message(
                chat_id,
                f"Role updated to {new_role} ✅"
            )

            return {
                "status": "role updated"
            }

    # ---------------- REGISTRATIONS LIST ----------------

    if user_text == "/registrations":

        if not is_admin(bale_id):

            send_message(
                chat_id,
                "شما دسترسی ادمین ندارید ❌"
            )

            return {
                "status": "forbidden"
            }

        registrations = get_all_registrations()

        if not registrations:

            send_message(
                chat_id,
                "هیچ ثبت‌نامی وجود ندارد ❌"
            )

            return {
                "status": "empty"
            }

        text = "لیست ثبت‌نام‌ها 👇\n\n"

        for reg in registrations:

            text += (
                f"ID: {reg.id}\n"
                f"دانش‌آموز: {reg.student_name}\n"
                f"پایه: {reg.grade}\n"
                f"تلفن: {reg.parent_phone}\n"
                f"وضعیت: {reg.status}\n\n"
            )

        send_message(chat_id, text)

        return {
            "status": "registrations list"
        }

    # ---------------- ACCEPT ----------------

    if user_text.startswith("/accept"):

        if not is_admin(bale_id):

            send_message(
                chat_id,
                "شما ادمین نیستید ❌"
            )

            return {
                "status": "forbidden"
            }

        parts = user_text.split()

        if len(parts) == 2:

            registration_id = int(parts[1])

            update_registration_status(
                registration_id,
                "accepted"
            )

            send_message(
                chat_id,
                "ثبت‌نام تایید شد ✅"
            )

            return {
                "status": "accepted"
            }

    # ---------------- REJECT ----------------

    if user_text.startswith("/reject"):

        if not is_admin(bale_id):

            send_message(
                chat_id,
                "شما ادمین نیستید ❌"
            )

            return {
                "status": "forbidden"
            }

        parts = user_text.split()

        if len(parts) == 2:

            registration_id = int(parts[1])

            update_registration_status(
                registration_id,
                "rejected"
            )

            send_message(
                chat_id,
                "ثبت‌نام رد شد ❌"
            )

            return {
                "status": "rejected"
            }

    # ---------------- START REGISTRATION ----------------

    if user_text == "ثبت نام":

        update_user_state(
            bale_id,
            "waiting_for_student_name"
        )

        send_message(
            chat_id,
            "لطفاً نام دانش‌آموز را وارد کنید 👇"
        )

        return {
            "status": "waiting for student name"
        }

    # ---------------- STUDENT NAME ----------------

    if current_state == "waiting_for_student_name":

        registration_data[bale_id] = {
            "student_name": user_text
        }

        update_user_state(
            bale_id,
            "waiting_for_grade"
        )

        send_message(
            chat_id,
            "پایه تحصیلی را وارد کنید 👇"
        )

        return {
            "status": "waiting for grade"
        }

    # ---------------- GRADE ----------------

    if current_state == "waiting_for_grade":

        registration_data[bale_id]["grade"] = user_text

        update_user_state(
            bale_id,
            "waiting_for_phone"
        )

        send_message(
            chat_id,
            "شماره تماس ولی را وارد کنید 👇"
        )

        return {
            "status": "waiting for phone"
        }

    # ---------------- PHONE ----------------

    if current_state == "waiting_for_phone":

        registration_data[bale_id]["parent_phone"] = user_text

        student_name = registration_data[bale_id]["student_name"]

        grade = registration_data[bale_id]["grade"]

        parent_phone = registration_data[bale_id]["parent_phone"]

        create_registration(
            parent_bale_id=bale_id,
            student_name=student_name,
            grade=grade,
            parent_phone=parent_phone
        )

        update_user_state(
            bale_id,
            ""
        )

        del registration_data[bale_id]

        send_message(
            chat_id,
            "ثبت‌نام کامل انجام شد ✅"
        )

        return {
            "status": "registration completed"
        }

    # ---------------- AI RESPONSE ----------------

    bot_response = generate_response(
        user_text,
        role=user_role
    )

    send_message(chat_id, bot_response)

    return {
        "status": "success"
    }


@router.get("/")
def bale_home():

    return {
        "message": "Bale Bot API Running"
    }