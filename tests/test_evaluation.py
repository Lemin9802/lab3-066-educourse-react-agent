from evaluation.run_evaluation import evaluate_answer


def test_simple_course_list_does_not_match_vietnamese_substrings():
    result = evaluate_answer(
        "simple_001",
        "Hiện tại, không có khóa học nào được cung cấp bởi trung tâm.",
    )

    assert result["passed"] is False


def test_web_course_without_slots_is_detected():
    result = evaluate_answer(
        "course_002",
        "Hiện tại không có lớp Web Beginner buổi tối nào còn chỗ.",
    )

    assert result["passed"] is True


def test_invalid_coupon_is_detected_without_diacritic_sensitive_matching():
    result = evaluate_answer(
        "failure_001",
        "Mã FAKECODE không hợp lệ nên không có giảm giá.",
    )

    assert result["passed"] is True
