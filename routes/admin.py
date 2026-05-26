from fastapi import APIRouter
from fastapi import Request
from fastapi import Form

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import Jinja2Templates

from services.registration_service import (
    get_all_registrations,
    update_registration_status,
    get_registrations_count,
    get_accepted_count,
    get_rejected_count,
    get_pending_count,
    search_registrations
)

router = APIRouter(prefix="/admin")

templates = Jinja2Templates(directory="templates")


# ---------------- LOGIN PAGE ----------------

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# ---------------- LOGIN ACTION ----------------

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    if username == "admin" and password == "1234":

        request.session["admin"] = True

        return RedirectResponse(
            url="/admin/registrations",
            status_code=303
        )

    return HTMLResponse(
        content="""
        <h2>Login Failed</h2>
        """,
        status_code=401
    )


# ---------------- LOGOUT ----------------

@router.get("/logout")
def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/admin/login",
        status_code=303
    )


# ---------------- REGISTRATIONS ----------------

@router.get(
    "/registrations",
    response_class=HTMLResponse
)
def registrations_list(
    request: Request,
    search: str = ""
):

    if not request.session.get("admin"):

        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )

    # آمار همیشه ساخته شود
    total_count = get_registrations_count()

    accepted_count = get_accepted_count()

    rejected_count = get_rejected_count()

    pending_count = get_pending_count()

    # جستجو
    if search:

        registrations = search_registrations(search)

    else:

        registrations = get_all_registrations()

    return templates.TemplateResponse(
        request=request,
        name="registrations.html",
        context={
            "registrations": registrations,
            "total_count": total_count,
            "accepted_count": accepted_count,
            "rejected_count": rejected_count,
            "pending_count": pending_count,
            "search": search
        }
    )


# ---------------- ACCEPT ----------------

@router.get("/accept/{registration_id}")
def accept_registration(
    request: Request,
    registration_id: int
):

    if not request.session.get("admin"):

        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )

    update_registration_status(
        registration_id,
        "accepted"
    )

    return RedirectResponse(
        url="/admin/registrations",
        status_code=303
    )


# ---------------- REJECT ----------------

@router.get("/reject/{registration_id}")
def reject_registration(
    request: Request,
    registration_id: int
):

    if not request.session.get("admin"):

        return RedirectResponse(
            url="/admin/login",
            status_code=303
        )

    update_registration_status(
        registration_id,
        "rejected"
    )

    return RedirectResponse(
        url="/admin/registrations",
        status_code=303
    )