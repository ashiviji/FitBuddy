from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    TIP_MODEL,
    DEMO_MODE
)


def generate_nutrition_tip_with_flash(goal):

    if not GEMINI_API_KEY or DEMO_MODE:

        return (
            f"General wellness tip for {goal}: "
            "prioritize regular meals, hydration, "
            "a varied diet with protein-rich foods, "
            "fruits and vegetables, and adequate recovery. "
            "For individual nutrition needs, consult "
            "a qualified professional."
        )

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    prompt = f"""

Give one concise and practical
nutrition or recovery tip related
to the fitness goal:

{goal}

Keep it general and age-appropriate.

Do not prescribe restrictive diets
or supplements.

Maximum 80 words.
"""

    response = client.models.generate_content(

        model=TIP_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=0.5,

            max_output_tokens=500
        )
    )

    return (
        response.text
        or
        "Stay hydrated and prioritize "
        "balanced meals and adequate recovery."
    )