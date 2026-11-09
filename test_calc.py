import pytest
from calc import CalculatorError, calculate, main, parse_number


@pytest.mark.parametrize(
    ("left", "operator", "right", "expected"),
    [(2, "+", 3, 5), (5, "-", 3, 2), (2, "*", 3, 6), (8, "/", 2, 4)],
)
def test_operations(left, operator, right, expected):
    assert calculate(left, operator, right) == expected


def test_unknown_operator():
    with pytest.raises(CalculatorError):
        calculate(1, "%", 2)


def test_main_prints_result(capsys):
    assert main(["8", "/", "2"]) == 0
    assert capsys.readouterr().out.strip() == "4.0"


def test_main_reports_unknown_operator(capsys):
    assert main(["1", "%", "2"]) == 1
    assert "unknown operator" in capsys.readouterr().err


def test_parse_number():
    assert parse_number("2.5") == 2.5
    with pytest.raises(CalculatorError):
        parse_number("abc")


def test_main_reports_invalid_left_number(capsys):
    assert main(["abc", "+", "2"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == "error: invalid number: abc"


def test_main_reports_invalid_right_number(capsys):
    assert main(["2", "+", "xyz"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.strip() == "error: invalid number: xyz"


def test_parse_number_error_uses_original_text():
    with pytest.raises(CalculatorError) as info:
        parse_number("1_x")
    assert str(info.value) == "invalid number: 1_x"


def test_parse_number_accepts_nan_and_inf():
    import math

    assert math.isnan(parse_number("nan"))
    assert parse_number("inf") == float("inf")
    assert parse_number("1_000") == 1000.0


@pytest.mark.parametrize(
    ("argv", "bad"),
    [(["abc", "+", "2"], "abc"), (["2", "+", "xyz"], "xyz")],
)
def test_cli_invalid_number_exits_1_without_traceback(argv, bad):
    import subprocess
    import sys
    from pathlib import Path

    script = Path(__file__).resolve().parent / "calc.py"
    proc = subprocess.run(
        [sys.executable, str(script), *argv],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 1
    assert proc.stdout == ""
    assert proc.stderr.strip() == f"error: invalid number: {bad}"
    assert "Traceback" not in proc.stderr


def test_cli_valid_input_still_works():
    import subprocess
    import sys
    from pathlib import Path

    script = Path(__file__).resolve().parent / "calc.py"
    proc = subprocess.run(
        [sys.executable, str(script), "8", "/", "2"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == "4.0"
