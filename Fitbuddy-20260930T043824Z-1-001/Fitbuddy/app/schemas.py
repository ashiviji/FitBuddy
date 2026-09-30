from pydantic import (
    BaseModel,
    Field,
    field_validator
)


class UserInput(BaseModel):

    username: str = Field(
        min_length=1,
        max_length=100
    )

    user_id: str = Field(
        min_length=1,
        max_length=100
    )

    age: int = Field(
        ge=13,
        le=120
    )

    weight: float = Field(
        gt=0,
        le=500
    )

    goal: str = Field(
        min_length=1,
        max_length=100
    )

    intensity: str

    @field_validator("intensity")
    @classmethod
    def validate_intensity(cls, value):

        value = value.lower()

        if value not in {
            "low",
            "medium",
            "high"
        }:

            raise ValueError(
                "Intensity must be low, medium, or high"
            )

        return value


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=1,
        max_length=100
    )

    feedback: str = Field(
        min_length=3,
        max_length=2000
    )