from menu import add_habit, checkin
from menu import valid_date, calcul_streak
from menu import file_loading, file_saving
from datetime import date

def test_add_habit():
    habits = []
    habit = add_habit(habits, "Exercise", 5, 0)
    assert len(habits) == 1
    assert habit['habit_name'] == "Exercise"
    assert habit['goal'] == 5
    assert habit['id'] == 1

def test_valid_date():
    assert valid_date("2023-10-10") == date(2023, 10, 10)
    assert valid_date("2025-10-10") is None  # Date future
    assert valid_date("invalid-date") is None

def test_checkin():
    habits = [
        {'id': 1, 'habit_name': 'Exercise', 'goal': 5, 'log': [], 'current_streak': 0}
    ]
    result1 = checkin(habits, 1, date(2023, 10, 10))
    assert result1['status'] == 1 or result1['status'] == 2
    assert date(2023, 10, 10) in habits[0]['log']

    result2 = checkin(habits, 1, date(2023, 10, 10))
    assert result2['status'] == 0  # déjà loggé

    result3 = checkin(habits, 2, date(2023, 10, 10))
    assert result3['status'] == -1  # habit non trouvé

def test_calcul_streak():
    assert calcul_streak([]) == 0
    assert calcul_streak([date(2023, 10, 10)]) == 1
    assert calcul_streak([date(2023, 10, 10), date(2023, 10, 9)]) == 2
    assert calcul_streak([date(2023, 10, 10), date(2023, 10, 8)]) == 1
