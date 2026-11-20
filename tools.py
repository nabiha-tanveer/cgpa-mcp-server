
import os

def marks_to_grade_points(marks: int) -> float | str:
    """Convert a course's marks (0-100) into PUCIT grade points.
    Use this whenever the student gives marks for a course and you need the
    grade point (e.g. 78 marks -> 3.3). Call it once per course before
    calculating a semester GPA. Do not convert marks yourself.
    """
    if not isinstance(marks, int) or marks < 0 or marks > 100:
        return "Error: marks must be a whole number between 0 and 100"
    if marks >= 85:
        return 4.0
    if marks >= 80:
        return 3.7
    if marks >= 75:
        return 3.3
    if marks >= 70:
        return 3.0
    if marks >= 65:
        return 2.7
    if marks >= 61:
        return 2.3
    if marks >= 58:
        return 2.0
    if marks >= 55:
        return 1.7
    if marks >= 50:
        return 1.0
    return 0.0


def calculate_semester_gpa(
    grade_points: list[float], credit_hours: list[float]
) -> float | str:
    """Calculate one semester's credit-weighted GPA.

    Use this after you have the grade points and credit hours for every
    course in the semester. The two lists must be the same length and in the
    same course order. Never average grade points yourself.
    """
    if not grade_points or not credit_hours:
        return "Error: grade_points and credit_hours cannot be empty"
    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must have the same length"
    if any(g < 0 or g > 4.0 for g in grade_points):
        return "Error: grade points must be between 0.0 and 4.0"
    if any(c <= 0 for c in credit_hours):
        return "Error: credit hours must be greater than 0"

    total_points = sum(g * c for g, c in zip(grade_points, credit_hours))
    total_credits = sum(credit_hours)
    return round(total_points / total_credits, 2)

def calculate_new_cgpa(
    current_cgpa: float,
    completed_credit_hours: float,
    semester_gpa: float,
    semester_credit_hours: float,
) -> float | str:
    """Project the student's new CGPA after one more semester.

    Use this when the student has a current CGPA and completed credit hours
    and asks where they will end up after a semester with a given GPA.
    Never compute the CGPA yourself.
    """
    if current_cgpa < 0 or current_cgpa > 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0"
    if semester_gpa < 0 or semester_gpa > 4.0:
        return "Error: semester_gpa must be between 0.0 and 4.0"
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative"
    if semester_credit_hours <= 0:
        return "Error: semester_credit_hours must be greater than 0"

    total_points = current_cgpa * completed_credit_hours + semester_gpa * semester_credit_hours
    total_credits = completed_credit_hours + semester_credit_hours
    return round(total_points / total_credits, 2)


def required_gpa_for_target(
    target_cgpa: float,
    current_cgpa: float,
    completed_credit_hours: float,
    remaining_credit_hours: float,
) -> float | str:
    """Calculate the GPA the student needs over the remaining credit hours
    to reach a target CGPA.

    Use this when the student wants to reach or graduate with a target CGPA.
    The result can be above 4.0, which means the target is impossible over
    that many credit hours. Never compute it yourself.
    """
    if target_cgpa < 0 or target_cgpa > 4.0:
        return "Error: target_cgpa must be between 0.0 and 4.0"
    if current_cgpa < 0 or current_cgpa > 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0"
    if completed_credit_hours < 0:
        return "Error: completed_credit_hours cannot be negative"
    if remaining_credit_hours <= 0:
        return "Error: remaining_credit_hours must be greater than 0"

    needed_points = target_cgpa * (completed_credit_hours + remaining_credit_hours)
    current_points = current_cgpa * completed_credit_hours
    return round((needed_points - current_points) / remaining_credit_hours, 2)


COURSES = {
    1: [("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0)],
    2: [("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5)],
    3: [("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5)],
    4: [("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5)],
    5: [("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5)],
    6: [("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5)],
    7: [("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5)],
    8: [("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5)],
}


def get_semester_courses(semester: int) -> str:
    """List the courses and credit hours for one semester (1 to 8) of the
    BS Computer Science scheme.

    Use this when the student asks what courses a semester has, or when you
    need the credit hour of each course to calculate a semester GPA. Math
    Deficiency courses (MD-001, MD-002) are non-credit and not included.
    """
    if semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    lines = [f"{code} | {name} | {ch} credit hours" for code, name, ch in COURSES[semester]]
    total = sum(ch for _, _, ch in COURSES[semester])
    lines.append(f"Total: {total} credit hours")
    return "\n".join(lines)



def get_remaining_credit_hours(current_semester: int, through_semester: int = 8) -> float | str:
    """Total the graded credit hours from current_semester up to and
    including through_semester ( i.e. graduation).

    Use this to get remaining_credit_hours before calling
    required_gpa_for_target. If the required GPA comes out above 4.0, call
    this again with a later through_semester to widen the window, e.g.
    (5, 5), then (5, 6), then (5, 7).
    """
    if current_semester not in COURSES or through_semester not in COURSES:
        return "Error: semester must be between 1 and 8"
    if through_semester < current_semester:
        return "Error: through_semester cannot be before current_semester"
    total = sum(
        ch
        for sem in range(current_semester, through_semester + 1)
        for _, _, ch in COURSES[sem]
    )
    return round(total, 1)


def save_report(filename: str, content: str) -> str:
    """Save a text summary (GPA result, projected CGPA or a target plan)
    to a file inside the reports folder.

    Use this only after the student has asked you to save something. Never
    save on your own.
    """
    name = os.path.basename(filename.strip())
    if not name:
        return "Error: filename cannot be empty"
    if not content.strip():
        return "Error: content cannot be empty"
    if not name.endswith(".txt"):
        name += ".txt"
    os.makedirs("reports", exist_ok=True)
    path = os.path.join("reports", name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Report saved to {path}"