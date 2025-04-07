from utils import valid_date, calcul_streak

def add_habit(habits, hb_name, goal: int, habit_count: int):
    habit = {'id': habit_count + 1, 'habit_name': hb_name, 'goal': goal, 'log': [], 'current_streak': 0}
    habits.append(habit)

def checkin(habits, input_id: int, date):
    for habit in habits:
        if habit['id'] == input_id:
            if date not in habit['log']:
                habit['log'].append(date)
                print(f'Habit {habit["habit_name"]} logged for {date}')

                streak = calcul_streak(habit['log'])
                habit['current_streak'] = streak
                if habit['current_streak'] == habit['goal']:
                    print(f"Congratulations! Goal streak reached!")
                    return 2
                else:
                    print(f"Current streak: {habit['current_streak']}/{habit['goal']}")
                    return 1

            else:
                print(f"Habit {habit['habit_name']} already logged for {date}")
                return 0
    print("Habit not found")
    return -1

def generate_report(habits):
    print("\n--- Habit Report ---")
    for habit in habits:
        print(f"{habit['id']} - {habit['habit_name']}: {habit['current_streak']} / {habit['goal']}")
    print("-------------------")
