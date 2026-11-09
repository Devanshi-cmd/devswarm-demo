import pytest
from calc import CalculatorError, calculate, main


@pytest.mark.parametrize(
    ("left", "operator", "right", "expected"),
    [
        (2, "+", 3, 5),
        (5, "-", 3, 2),
        (2, "*", 3, 6),
        (8, "/", 2, 4),
        (2, "^", 3, 8),
        (2, "^", 0, 1),
        (9, "^", 0.5, 3.0),
        (2, "^", -1, 0.5),
    ],
)
def test_operations(left, operator, right, expected):
    assert calculate(left, operator, right) == expected


def test_unknown_operator():
    with pytest.raises(CalculatorError):
        calculate(1, "%", 2)


def test_power_zero_to_negative_power_raises():
    with pytest.raises(CalculatorError):
        calculate(0, "^", -1)


def test_power_overflow_raises():
    with pytest.raises(CalculatorError):
        calculate(10.0, "^", 400.0)


def test_power_negative_base_fractional_exponent_raises():
    with pytest.raises(CalculatorError):
        calculate(-8, "^", 1 / 3)


def test_main_prints_result(capsys):
    assert main(["8", "/", "2"]) == 0
    assert capsys.readouterr().out.strip() == "4.0"


def test_main_reports_unknown_operator(capsys):
    assert main(["1", "%", "2"]) == 1
    assert "unknown operator" in capsys.readouterr().err


def test_main_power(capsys):
    assert main(["2", "^", "3"]) == 0
    assert capsys.readouterr().out.strip() == "8.0"


def test_main_reports_power_error(capsys):
    assert main(["0", "^", "-1"]) == 1
    assert "error:" in capsys.readouterr().err


def test_main_power_overflow_reports_error(capsys):
    assert main(["10", "^", "400"]) == 1
    assert "error:" in capsys.readouterr().err


def test_main_power_complex_result_reports_error(capsys):
    assert main(["-8", "^", "0.5"]) == 1
    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "j" not in captured.out


def test_power_negative_base_integer_exponent_is_real():
    assert calculate(-2, "^", 3) == -8


def test_power_cli_subprocess_prints_8_0():
    import subprocess
    import sys
    from pathlib import Path

    script = Path(__file__).parent / "calc.py"
    completed = subprocess.run(
        [sys.executable, str(script), "2", "^", "3"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0
    assert completed.stdout.strip() == "8.0"
    assert "Traceback" not in completed.stderr
