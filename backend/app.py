from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    return jsonify(db.get_all_students()), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.json

    name = student_data["name"]
    course = student_data["course"]
    mark = None
    if student_data.get("mark"):
        mark = student_data["mark"]
        if mark < 0 or mark > 100:
            return jsonify({"error": "Mark out of range"}), 404

    if not name:
        return jsonify({"error": "Name not provided"}), 404
    elif not course:
        return jsonify({"error": "Course not provided"}), 404

    student = db.insert_student(name, course, mark)

    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json

    student = db.update_student(student_id, name=student_data["name"], course=student_data["course"], mark=student_data["mark"])
    
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student = db.delete_student(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    if len(students) == 0:
        return jsonify({"error": "Zero students in database"}), 404

    marks = []
    marks_sum = 0
    for student in students:
        if not student["mark"]:
            continue
        marks.append(student["mark"])
        marks_sum += student["mark"]
    return jsonify({
        "count": len(marks),
        "average": marks_sum / len(marks),
        "min": min(marks),
        "max": max(marks)
    }), 200


@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)