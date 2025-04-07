from project import add_habit, checkin, valid_date, calcul_streak, file_loading, file_saving
from datetime import date, datetime

def test_add_habit():
    habits = []
    assert add_habit(habits, "Exercise", 5, 0) == 1
    assert len(habits) == 1
    assert habits[0]['habit_name'] == "Exercise"
    assert habits[0]['goal'] == 5

def test_valid_date():
    assert valid_date("2023-10-10") == date(2023, 10, 10)
    assert valid_date("2023-10-10") is not None
    assert valid_date("2025-10-10") is None  # Future date
    assert valid_date("invalid-date") is None  # Invalid format

def test_checkin():
    habits = [
        {'id': 1, 'habit_name': 'Exercise', 'goal': 5, 'log': [], 'current_streak': 0}
    ]
    assert checkin(habits, 1, date(2023, 10, 10)) == 1  # Habit logged, streak continues
    assert checkin(habits, 1, date(2023, 10, 10)) == 0  # Habit already logged
    assert checkin(habits, 2, date(2023, 10, 10)) == -1  # Habit not found

def test_calcul_streak():
    assert calcul_streak([]) == 0  # No logs
    assert calcul_streak([date(2023, 10, 10)]) == 1  # Single log
    assert calcul_streak([date(2023, 10, 10), date(2023, 10, 9)]) == 2  # Consecutive days
    assert calcul_streak([date(2023, 10, 10), date(2023, 10, 8)]) == 1  # Non-consecutive days
