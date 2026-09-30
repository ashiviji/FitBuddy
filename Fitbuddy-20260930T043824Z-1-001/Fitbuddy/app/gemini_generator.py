from google import genai
from google.genai import types

from app.config import (
    GEMINI_API_KEY,
    WORKOUT_MODEL,
    DEMO_MODE
)


def _client():

    if not GEMINI_API_KEY:

        return None

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


def _demo_plan(
    username,
    goal,
    intensity
):

    return f"""
7-DAY FITBUDDY WORKOUT PLAN

User: {username}
Goal: {goal}
Intensity: {intensity.title()}

Day 1 – Full Body

Warm-up:
5–10 minutes of easy movement.

Main Workout:
Squat pattern, push movement,
pull movement and core work.

Cooldown:
Gentle stretching and relaxed breathing.


Day 2 – Cardio & Mobility

Warm-up:
5 minutes.

Main Workout:
Moderate cardio and mobility exercises.

Cooldown:
Easy walking and stretching.


Day 3 – Upper Body

Warm-up:
5–10 minutes.

Main Workout:
Push, pull, shoulder and core movements.

Cooldown:
Gentle upper-body stretching.


Day 4 – Recovery

Easy walking or light mobility.

Keep the session comfortable.


Day 5 – Lower Body

Warm-up:
5–10 minutes.

Main Workout:
Squat/lunge pattern,
hip-hinge pattern,
calf work and core.

Cooldown:
Gentle stretching.


Day 6 – Cardio & Core

Warm-up:
5 minutes.

Main Workout:
Comfortable cardio intervals
and simple core exercises.

Cooldown:
Easy movement and breathing.


Day 7 – Rest & Recovery

Rest, sleep well, hydrate
and perform light mobility if comfortable.


SAFETY NOTE

Start gradually.
Use good technique.
Stop if you experience pain,
dizziness or unusual symptoms.
"""


def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):

    client = _client()

    if client is None or DEMO_MODE:

        return _demo_plan(
            username,
            goal,
            intensity
        )

    prompt = f"""

Create a safe, general 7-day fitness plan.

User information:

Name: {username}

Age: {age}

Weight: {weight} kg

Goal: {goal}

Preferred intensity: {intensity}


Requirements:

1. Give Day 1 through Day 7.

2. For every active day include:
   - Warm-up
   - Main workout
   - Cooldown or recovery

3. Give simple exercise names.

4. Give sets/repetitions or duration
   where appropriate.

5. Include rest/recovery days.

6. Keep recommendations general.

7. Do not diagnose medical conditions.

8. Do not recommend extreme dieting
   or unsafe exercise.

9. Tell the user to stop if they experience
   pain, dizziness or unusual symptoms.

10. Use clear plain-text headings.
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
        or
        _demo_plan(
            username,
            goal,
            intensity
        )
    )