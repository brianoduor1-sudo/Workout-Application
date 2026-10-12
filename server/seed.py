#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Workout, Exercise, WorkoutExercise

with app.app_context():
    print("Clearing database tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding Exercises...")
    pushups = Exercise(name="Push-ups", category="Strength", equipment_needed=False)
    bench_press = Exercise(name="Bench Press", category="Strength", equipment_needed=True)
    running = Exercise(name="Treadmill Running", category="Cardio", equipment_needed=True)
    plank = Exercise(name="Plank", category="Strength", equipment_needed=False)

    db.session.add_all([pushups, bench_press, running, plank])
    db.session.commit()

    print("Seeding Workouts...")
    workout1 = Workout(date=date(2026, 10, 10), duration_minutes=45, notes="Upper body day")
    workout2 = Workout(date=date(2026, 10, 12), duration_minutes=30, notes="Quick cardio & core")

    db.session.add_all([workout1, workout2])
    db.session.commit()

    print("Seeding WorkoutExercises...")
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=pushups.id, reps=15, sets=4)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=bench_press.id, reps=10, sets=3)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=running.id, duration_seconds=1200)
    we4 = WorkoutExercise(workout_id=workout2.id, exercise_id=plank.id, sets=3, duration_seconds=60)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Seeding completed successfully!")