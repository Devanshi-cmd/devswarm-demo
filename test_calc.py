import pytest
from calc import CalculatorError, calculate, main


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


@pytest.mark.parametrize("right", [0, 0.0, -0.0])
def test_division_by_zero_raises(right):
    with pytest.raises(CalculatorError, match="division by zero"):
        calculate(1, "/", right)


def test_main_reports_division_by_zero(capsys):
    assert main(["1", "/", "0"]) == 1
    captured = capsys.readouterr()
    assert "division by zero" in captured.err
    assert "Traceback" not in captured.err
    assert captured.out == ""


def test_cli_division_by_zero_exits_with_status_1():
    import subprocess
    import sys
    from pathlib import Path

    script = Path(__file__).parent / "calc.py"
    proc = subprocess.run(
        [sys.executable, str(script), "1", "/", "0"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 1
    assert "division by zero" in proc.stderr
    assert "Traceback" not in proc.stderr
    assert proc.stdout == ""
