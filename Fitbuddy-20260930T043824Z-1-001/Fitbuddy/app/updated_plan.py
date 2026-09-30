from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    WORKOUT_MODEL,
    DEMO_MODE
)


def update_workout_plan(
    original_plan,
    feedback,
    goal,
    intensity
):

    if not GEMINI_API_KEY or DEMO_MODE:

        return (
            original_plan
            + "\n\n"
            + "FEEDBACK UPDATE\n"
            + f"Requested change: {feedback}\n\n"
            + "Demo mode: review the requested "
              "change with a qualified professional "
              "before making major changes."
        )

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    prompt = f"""

Revise the following 7-day fitness plan
using the user's feedback.

Goal:
{goal}

Intensity:
{intensity}


ORIGINAL PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


Return a complete revised Day 1–Day 7 plan.

Keep the recommendations general,
safe and realistic.

Include recovery/rest.

Do not recommend extreme dieting,
dangerous challenges or exercising
through pain.
"""

    response = client.models.generate_content(

        model=WORKOUT_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=0.6,

            max_output_tokens=5000
        )
    )

    return (
        response.text
        or original_plan
    )