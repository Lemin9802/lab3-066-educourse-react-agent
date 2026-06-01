from typing import Any, Dict, List, Optional


COURSES: Dict[str, Dict[str, Any]] = {
    "PY101": {
        "name": "Python Beginner",
        "topic": "Python",
        "level": "beginner",
        "schedule": "evening",
        "tuition_vnd": 1500000,
        "slots_left": 5,
    },
    "PY201": {
        "name": "Python Data Analysis",
        "topic": "Python",
        "level": "intermediate",
        "schedule": "weekend",
        "tuition_vnd": 2200000,
        "slots_left": 2,
    },
    "WEB101": {
        "name": "Web Development Beginner",
        "topic": "Web",
        "level": "beginner",
        "schedule": "evening",
        "tuition_vnd": 1200000,
        "slots_left": 0,
    },
    "DS101": {
        "name": "Data Science Foundation",
        "topic": "Data Science",
        "level": "beginner",
        "schedule": "weekend",
        "tuition_vnd": 2500000,
        "slots_left": 3,
    },
    "AI101": {
        "name": "AI for Beginners",
        "topic": "AI",
        "level": "beginner",
        "schedule": "evening",
        "tuition_vnd": 1800000,
        "slots_left": 4,
    },
}

COUPONS: Dict[str, int] = {
    "STUDENT10": 10,
    "EARLYBIRD": 15,
    "WELCOME5": 5,
    "NONE": 0,
}


def _course_result(course_id: str, course: Dict[str, Any]) -> Dict[str, Any]:
    return {"course_id": course_id, **course}


def search_courses(
    topic: str, level: str, schedule: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find courses matching a topic, level, and optional schedule.
    """
    matches: List[Dict[str, Any]] = []
    for course_id, course in COURSES.items():
        if (
            course["topic"] == topic
            and course["level"] == level
            and (schedule is None or course["schedule"] == schedule)
        ):
            matches.append(_course_result(course_id, course))

    return {"matches": matches}


def check_class_slots(course_id: str) -> Dict[str, Any]:
    """
    Return whether a course exists and still has available seats.
    """
    course = COURSES.get(course_id)
    if course is None:
        return {
            "course_id": course_id,
            "available": False,
            "slots_left": 0,
            "error": "Course not found.",
        }

    slots_left = course["slots_left"]
    return {
        "course_id": course_id,
        "available": slots_left > 0,
        "slots_left": slots_left,
    }


def get_coupon(coupon_code: str) -> Dict[str, Any]:
    """
    Validate a coupon code and return its discount percentage.
    """
    if coupon_code not in COUPONS:
        return {
            "valid": False,
            "coupon_code": coupon_code,
            "discount_percent": 0,
            "error": "Coupon code is invalid.",
        }

    return {
        "valid": True,
        "coupon_code": coupon_code,
        "discount_percent": COUPONS[coupon_code],
    }


def calculate_tuition(course_id: str, coupon_code: str = "NONE") -> Dict[str, Any]:
    """
    Calculate tuition for a course after applying a valid coupon.
    """
    course = COURSES.get(course_id)
    if course is None:
        return {
            "course_id": course_id,
            "error": "Course not found.",
        }

    coupon = get_coupon(coupon_code)
    if not coupon["valid"]:
        return {
            "course_id": course_id,
            "coupon_code": coupon["coupon_code"],
            "error": "Coupon code is invalid.",
        }

    original_tuition = course["tuition_vnd"]
    discount_percent = coupon["discount_percent"]
    discount_vnd = original_tuition * discount_percent // 100
    return {
        "course_id": course_id,
        "coupon_code": coupon["coupon_code"],
        "original_tuition_vnd": original_tuition,
        "discount_percent": discount_percent,
        "discount_vnd": discount_vnd,
        "final_tuition_vnd": original_tuition - discount_vnd,
    }


TOOLS: List[Dict[str, Any]] = [
    {
        "name": "search_courses",
        "description": (
            "Find courses by topic and level, with an optional schedule. "
            "Arguments: topic (string), level (string), schedule (optional string, "
            "such as 'evening' or 'weekend'). Returns a dictionary containing a "
            "matches list."
        ),
        "function": search_courses,
    },
    {
        "name": "check_class_slots",
        "description": (
            "Check whether a specific course still has seats. Arguments: course_id "
            "(string, such as 'PY101'). Returns available and slots_left."
        ),
        "function": check_class_slots,
    },
    {
        "name": "get_coupon",
        "description": (
            "Validate a coupon code. Arguments: coupon_code (string, such as "
            "'STUDENT10'). Returns valid and discount_percent."
        ),
        "function": get_coupon,
    },
    {
        "name": "calculate_tuition",
        "description": (
            "Calculate the final tuition after applying a coupon. Arguments: "
            "course_id (string) and coupon_code (string; use 'NONE' when there is "
            "no coupon). Returns original tuition, discount, and final tuition in "
            "VND."
        ),
        "function": calculate_tuition,
    },
]
