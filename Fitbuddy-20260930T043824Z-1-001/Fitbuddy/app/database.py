from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)

from datetime import datetime

from app.config import DATABASE_URL


connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    username = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Float,
        nullable=False
    )

    goal = Column(
        String(100),
        nullable=False
    )

    intensity = Column(
        String(20),
        nullable=False
    )

    original_plan = Column(
        Text,
        nullable=True
    )

    updated_plan = Column(
        Text,
        nullable=True
    )

    nutrition_tip = Column(
        Text,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


def init_db():

    Base.metadata.create_all(
        bind=engine
    )


def save_user(data):

    db = SessionLocal()

    try:

        user = User(**data)

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    finally:

        db.close()


def get_user(user_id):

    db = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )

    finally:

        db.close()


def save_plan(
    user_id,
    plan,
    tip
):

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )

        if user:

            user.original_plan = plan

            user.nutrition_tip = tip

            db.commit()

    finally:

        db.close()


def update_plan(
    user_id,
    updated_plan,
    feedback
):

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )

        if user:

            user.updated_plan = updated_plan

            user.feedback = feedback

            db.commit()

    finally:

        db.close()


def get_all_users():

    db = SessionLocal()

    try:

        return (
            db.query(User)
            .order_by(
                User.created_at.desc()
            )
            .all()
        )

    finally:

        db.close()


def delete_user(user_id):

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )

        if user:

            db.delete(user)

            db.commit()

            return True

        return False

    finally:

        db.close()