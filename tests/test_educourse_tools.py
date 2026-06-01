from src.tools.educourse_tools import (
    TOOLS,
    calculate_tuition,
    check_class_slots,
    get_coupon,
    search_courses,
)


def test_search_courses_filters_topic_level_and_schedule():
    result = search_courses("Python", "beginner", "evening")

    assert [course["course_id"] for course in result["matches"]] == ["PY101"]


def test_search_courses_allows_omitting_schedule():
    result = search_courses("Python", "beginner")

    assert [course["course_id"] for course in result["matches"]] == ["PY101"]


def test_check_class_slots_reports_full_course():
    assert check_class_slots("WEB101") == {
        "course_id": "WEB101",
        "available": False,
        "slots_left": 0,
    }


def test_get_coupon_reports_invalid_code():
    assert get_coupon("FAKECODE") == {
        "valid": False,
        "coupon_code": "FAKECODE",
        "discount_percent": 0,
        "error": "Coupon code is invalid.",
    }


def test_calculate_tuition_applies_coupon():
    result = calculate_tuition("PY101", "STUDENT10")

    assert result["discount_vnd"] == 150000
    assert result["final_tuition_vnd"] == 1350000


def test_calculate_tuition_rejects_unknown_course():
    assert calculate_tuition("UNKNOWN", "STUDENT10") == {
        "course_id": "UNKNOWN",
        "error": "Course not found.",
    }


def test_tools_export_names_descriptions_and_callables():
    assert {tool["name"] for tool in TOOLS} == {
        "search_courses",
        "check_class_slots",
        "get_coupon",
        "calculate_tuition",
    }
    assert all(tool["description"] for tool in TOOLS)
    assert all(callable(tool["function"]) for tool in TOOLS)
