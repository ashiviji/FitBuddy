from fastapi import APIRouter, Request, Form

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
    JSONResponse
)

from fastapi.templating import Jinja2Templates

from app.schemas import (
    UserInput,
    FeedbackRequest
)

from app.database import (
    save_user,
    get_user,
    save_plan,
    update_plan,
    get_all_users,
    delete_user
)

from app.gemini_generator import (
    generate_workout_gemini
)

from app.gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from app.updated_plan import (
    update_workout_plan
)


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):

    try:

        data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        if get_user(data.user_id):

            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "error":
                    "That User ID already exists. "
                    "Use a different User ID."
                },
                status_code=400
            )

        user = save_user(
            data.model_dump()
        )

        plan = generate_workout_gemini(
            data.username,
            data.age,
            data.weight,
            data.goal,
            data.intensity
        )

        tip = generate_nutrition_tip_with_flash(
            data.goal
        )

        save_plan(
            user.user_id,
            plan,
            tip
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": get_user(user.user_id),
                "workout_plan": plan,
                "nutrition_tip": tip,
                "message": None
            }
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error":
                f"Could not generate the plan: {exc}"
            },
            status_code=500
        )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):

    try:

        req = FeedbackRequest(
            user_id=user_id,
            feedback=feedback
        )

        user = get_user(
            req.user_id
        )

        if not user:

            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={
                    "error": "User ID not found."
                },
                status_code=404
            )

        original = (
            user.original_plan
            or ""
        )

        revised = update_workout_plan(
            original,
            req.feedback,
            user.goal,
            user.intensity
        )

        update_plan(
            req.user_id,
            revised,
            req.feedback
        )

        updated_user = get_user(
            req.user_id
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": updated_user,
                "workout_plan": revised,
                "nutrition_tip":
                updated_user.nutrition_tip,
                "message":
                "Your plan was updated using the feedback."
            }
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": get_user(user_id),
                "workout_plan": "",
                "nutrition_tip": "",
                "message":
                f"Could not update plan: {exc}"
            },
            status_code=500
        )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": get_all_users()
        }
    )


@router.post(
    "/delete-user/{user_id}"
)
def remove_user(
    user_id: str
):

    delete_user(user_id)

    return RedirectResponse(
        "/view-all-users",
        status_code=303
    )


@router.get("/api/users")
def api_users():

    users = get_all_users()

    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
            "created_at": user.created_at
        }
        for user in users
    ]


@router.get(
    "/api/users/{user_id}"
)
def api_user(
    user_id: str
):

    user = get_user(
        user_id
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "User not found"
            },
            status_code=404
        )

    return {
        "user_id": user.user_id,
        "username": user.username,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "original_plan": user.original_plan,
        "updated_plan": user.updated_plan,
        "nutrition_tip": user.nutrition_tip,
        "feedback": user.feedback
    }


@router.get("/health")
def health():

    return {
        "status": "ok",
        "service": "FitBuddy"
    }