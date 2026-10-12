from datetime import datetime
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import (
    exercise_schema,
    exercises_schema,
    exercise_detail_schema,
    workout_schema,
    workouts_schema,
    workout_detail_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)


# Error Handlers
@app.errorhandler(ValidationError)
def handle_marshmallow_validation_error(err):
    return jsonify({"errors": err.messages}), 400


@app.errorhandler(ValueError)
def handle_value_error(err):
    return jsonify({"error": str(err)}), 400


# Workout Endpoints
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    return jsonify(workout_detail_schema.dump(workout)), 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    validated_data = workout_schema.load(data)
    
    new_workout = Workout(**validated_data)
    db.session.add(new_workout)
    db.session.commit()
    
    return jsonify(workout_schema.dump(new_workout)), 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404
    
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": f"Workout {id} successfully deleted"}), 200


# Exercise Endpoints
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise_by_id(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    return jsonify(exercise_detail_schema.dump(exercise)), 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    validated_data = exercise_schema.load(data)
    
    new_exercise = Exercise(**validated_data)
    db.session.add(new_exercise)
    db.session.commit()
    
    return jsonify(exercise_schema.dump(new_exercise)), 201


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404
    
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": f"Exercise {id} successfully deleted"}), 200


# Join Table Endpoint: Add exercise to workout
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return jsonify({"error": "Workout not found"}), 404

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return jsonify({"error": "Exercise not found"}), 404

    payload = request.get_json() or {}
    payload["workout_id"] = workout_id
    payload["exercise_id"] = exercise_id

    validated_data = workout_exercise_schema.load(payload)

    new_workout_exercise = WorkoutExercise(**validated_data)
    db.session.add(new_workout_exercise)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(new_workout_exercise)), 201


if __name__ == "__main__":
    app.run(port=5555, debug=True)