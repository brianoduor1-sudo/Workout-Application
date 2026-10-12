from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    
    # Schema Validations: Range check on numeric metrics
    reps = fields.Int(validate=validate.Range(min=0, error="Reps must be >= 0."))
    sets = fields.Int(validate=validate.Range(min=0, error="Sets must be >= 0."))
    duration_seconds = fields.Int(
        validate=validate.Range(min=0, error="Duration seconds must be >= 0.")
    )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    
    # Schema Validation 1: Length check on exercise name
    name = fields.Str(
        required=True,
        validate=validate.Length(min=2, error="Exercise name must be at least 2 characters."),
    )
    
    # Schema Validation 2: Category membership validation
    category = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["Cardio", "Strength", "Flexibility", "Balance", "HIIT"],
            error="Category must be one of: Cardio, Strength, Flexibility, Balance, HIIT.",
        ),
    )
    equipment_needed = fields.Bool(required=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    
    # Schema Validation: Positive duration check
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="Duration in minutes must be at least 1."),
    )
    notes = fields.Str(allow_none=True)


# Nested schemas for detail endpoints
class WorkoutExerciseDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()
    exercise = fields.Nested(ExerciseSchema(only=("id", "name", "category", "equipment_needed")))


class WorkoutDetailSchema(WorkoutSchema):
    workout_exercises = fields.Nested(WorkoutExerciseDetailSchema, many=True)


class ExerciseDetailSchema(ExerciseSchema):
    workouts = fields.Nested(WorkoutSchema(many=True), dump_only=True)


# Schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
exercise_detail_schema = ExerciseDetailSchema()

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_detail_schema = WorkoutDetailSchema()

workout_exercise_schema = WorkoutExerciseSchema()