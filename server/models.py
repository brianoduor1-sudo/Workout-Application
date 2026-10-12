from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    # Table Constraints: Unique name constraint
    __table_args__ = (
        CheckConstraint("length(name) >= 2", name="check_exercise_name_length"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # Relationships
    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan"
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True,
    )

    # Model Validation 1: Exercise Name
    @validates("name")
    def validate_name(self, key, value):
        if not value or not isinstance(value, str) or len(value.strip()) < 2:
            raise ValueError("Exercise name must be a string with at least 2 characters.")
        return value.strip()

    # Model Validation 2: Exercise Category
    @validates("category")
    def validate_category(self, key, value):
        allowed_categories = ["Cardio", "Strength", "Flexibility", "Balance", "HIIT"]
        if not value or value.capitalize() not in allowed_categories:
            raise ValueError(
                f"Category must be one of: {', '.join(allowed_categories)}"
            )
        return value.capitalize()


class Workout(db.Model):
    __tablename__ = "workouts"

    # Table Constraint: Positive duration_minutes
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="check_workout_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    workout_exercises = db.relationship(
        "WorkoutExercise", back_populates="workout", cascade="all, delete-orphan"
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True,
    )

    # Model Validation: Positive Duration
    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is None or not isinstance(value, int) or value <= 0:
            raise ValueError("Workout duration_minutes must be an integer greater than 0.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    # Table Constraints: Non-negative metrics
    __table_args__ = (
        CheckConstraint("reps >= 0", name="check_reps_non_negative"),
        CheckConstraint("sets >= 0", name="check_sets_non_negative"),
        CheckConstraint("duration_seconds >= 0", name="check_duration_seconds_non_negative"),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer, db.ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False
    )
    reps = db.Column(db.Integer, nullable=True, default=0)
    sets = db.Column(db.Integer, nullable=True, default=0)
    duration_seconds = db.Column(db.Integer, nullable=True, default=0)

    # Relationships
    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # Model Validation: Reps and Sets
    @validates("reps", "sets", "duration_seconds")
    def validate_metrics(self, key, value):
        if value is not None and (not isinstance(value, int) or value < 0):
            raise ValueError(f"{key} must be an integer greater than or equal to 0.")
        return value