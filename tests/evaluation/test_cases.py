TEST_CASES = [
    {
        "id": "simple_001",
        "query": "Trung tâm có những khóa học nào?",
        "expected": "List available courses from the fake course catalog.",
        "expected_tools": ["search_courses"],
        "success_criteria": [
            "Mentions multiple available course options.",
            "Does not invent courses outside the fake catalog.",
            "For the ReAct agent, uses search_courses or an equivalent catalog lookup.",
        ],
    },
    {
        "id": "course_001",
        "query": (
            "Em muốn học Python beginner buổi tối, dùng mã STUDENT10. "
            "Học phí cuối cùng là bao nhiêu?"
        ),
        "expected": "Find PY101, check available slots, validate STUDENT10, and calculate final tuition.",
        "expected_tools": [
            "search_courses",
            "check_class_slots",
            "get_coupon",
            "calculate_tuition",
        ],
        "success_criteria": [
            "Identifies PY101 or Python Beginner as the matching course.",
            "Confirms the course has available slots.",
            "Applies STUDENT10 as a 10 percent discount.",
            "Returns final tuition of 1,350,000 VND.",
        ],
    },
    {
        "id": "course_002",
        "query": "Em muốn học Web beginner buổi tối. Có lớp nào còn chỗ không?",
        "expected": "Detect WEB101 matches the request but has zero available slots.",
        "expected_tools": ["search_courses", "check_class_slots"],
        "success_criteria": [
            "Identifies WEB101 or Web Development Beginner as the matching course.",
            "Checks class availability before recommending the course.",
            "States clearly that the class has no available slots.",
            "Does not recommend WEB101 as currently enrollable.",
        ],
    },
    {
        "id": "course_003",
        "query": (
            "Em muốn học Data Science beginner cuối tuần, ngân sách 2.000.000 VND. "
            "Có phù hợp không?"
        ),
        "expected": "Find DS101 but detect its tuition exceeds the 2,000,000 VND budget.",
        "expected_tools": ["search_courses", "check_class_slots"],
        "success_criteria": [
            "Identifies DS101 or Data Science Foundation as the matching course.",
            "Mentions tuition of 2,500,000 VND.",
            "Compares tuition against the 2,000,000 VND budget.",
            "States that the course exceeds the student's budget.",
        ],
    },
    {
        "id": "course_004",
        "query": "Em muốn học AI beginner buổi tối, dùng mã EARLYBIRD. Tính học phí sau giảm.",
        "expected": "Find AI101, check slots, apply EARLYBIRD, and calculate tuition after 15 percent discount.",
        "expected_tools": [
            "search_courses",
            "check_class_slots",
            "get_coupon",
            "calculate_tuition",
        ],
        "success_criteria": [
            "Identifies AI101 or AI for Beginners as the matching course.",
            "Confirms the course has available slots.",
            "Applies EARLYBIRD as a 15 percent discount.",
            "Returns final tuition of 1,530,000 VND.",
        ],
    },
    {
        "id": "failure_001",
        "query": "Em muốn học Python nâng cao nhưng dùng mã FAKECODE. Có giảm giá không?",
        "expected": "Handle an unavailable advanced Python course request and an invalid coupon code.",
        "expected_tools": ["search_courses", "get_coupon"],
        "success_criteria": [
            "Does not claim that FAKECODE is valid.",
            "Explains that no matching advanced Python course exists in the fake catalog.",
            "Does not calculate a fake discounted tuition.",
            "Provides a useful alternative or next step.",
        ],
    },
]


def get_test_cases():
    return TEST_CASES
