from datetime import timedelta, date

def main():
    try:
        habits = file_loading()
        habit_counter = max(habit['id'] for habit in habits) if habits else 0
    except Exception:
        habits = []
        habit_counter = 0

    while True:
        print("\n--- Habit Tracker Menu ---")
        print("1. Add habit")
        print("2. Log a habit")
        print("3. Generate report")
        print("4. Save and Exit")

        choice = input("Choose a proposed option: ").strip()

        if choice == '1':
            print("-------------------")
            hb_name = input("Input the name of the habit: ").strip()
            try:
                goal = int(input("Input a goal (number of days): ").strip())
                add_habit(habits, hb_name, goal, habit_counter)
                habit_counter = habit_counter + 1
                print(f"Habit '{hb_name}' added!")

            except ValueError:
                print("Goal must be a number!")

        elif choice == '2':
            print("-------------------")
            if not habits:
                print("No habits added yet. Add one habit first.")
                continue
            print("Current habits: ")
            for habit in habits:
                print(f"{habit['id']} - {habit['habit_name']}")
            print("-------------------")

            while True:
                try:
                    input_id = int(input("Enter an existing ID of habit: ").strip())
                    habit_exists = any(habit['id'] == input_id for habit in habits)
                    if habit_exists:
                        break
                    else:
                        print("Habit not found. Enter a valid habit ID.")
                except ValueError:
                    print("Please enter a valid habit ID")

            day = valid_date(input("Enter a valid date (YYYY-MM-DD): ").strip())
            if day is not None:
                checkin(habits, input_id, day)
            else:
                print("Check-in cancelled due to invalid date.")

        elif choice == '3':
            print("-------------------")
            generate_report(habits)

        elif choice == '4':
            print("-------------------")
            print("Saving and exiting...")
            print(file_saving(habits))
            break
        else:
            print("-------------------")
            print("Invalid choice. Try again!")



def add_habit(habits, hb_name, goal: int, habit_count:int):
    habit = {'id': habit_count + 1, 'habit_name': hb_name, 'goal': goal, 'log': [], 'current_streak': 0}
    habits.append(habit)
    return 1


def valid_date(day_str):
    today = date.today()
    try:
        day = date.fromisoformat(day_str)  # return a date object
        if day > today:
            print("Date to be logged cannot be in the future")
            return None
        return day
    except ValueError:
        print("Invalid date format. Please follow YYYY-MM-DD.")
        return None


def checkin(habits, input_id:int, date: date):
    """to log in habit per date which gives different return codes depending each case
        0 : nothing logged
        -1: habit not found
        1: habit logged and streak still counting
        2: habit logged and goal achieved
    """

    for habit in habits:
        if habit['id'] == input_id:
            if date not in habit['log']:
                habit['log'].append(date)
                print(f'Habit {habit['habit_name']} logged for {date}')

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

def calcul_streak(log):
    # if log list is empty, return streak = 0
    if not log:
        return 0

    log.sort(reverse=True)  # Most recent day first
    streak = 1
    last_date = log[0]

    for i in range(1, len(log)):
        if last_date - log[i] == timedelta(days=1):
            streak += 1
            last_date = log[i]
        else:
            break

    return streak

def generate_report(habits):
    print("\n--- Habit Report ---")
    for habit in habits:
        print(f"{habit['id']} - {habit['habit_name']}: {habit['current_streak']} / {habit['goal']}")
    print("-------------------")

def file_saving(habits, filename = 'habits_log.txt'):
    try:
        with open(filename, 'w') as file: #allows automatically close a file, error handling implicitely
            for h in habits:
                log = []
                for date in h['log']:
                    log.append(date.isoformat()) #convert to string YYYY-MM-DD

                file.write(f"id: {h['id']}; habit: {h['habit_name']}; streak: {h['current_streak']}; goal: {h['goal']}; log: {log}\n") #separator is ';' to facillitate parsing
        return(f"Habits successfully saved to {filename}")

    except FileNotFoundError:
        print(f"File {filename} doesn't exist")
    except OSError as e: #operating ststem-related error : disk full or permission
        print(f"OSError: {e}")
    except Exception as e:
        return(f"Unexpected error: {e}")

def file_loading(filename='habits_log.txt'):
    habits = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                groups = line.strip().split(';')

                try:
                    id_index = next((i for i, part in enumerate(groups) if part.strip().startswith('id:')), None)
                except ValueError:
                    print("id: not found in the line")
                    return habits

                try:
                    habit_index = next((i for i, part in enumerate(groups) if part.strip().startswith('habit:')), None)

                except ValueError:
                    print("habit: not found in the line")
                    return habits

                try:
                    streak_index = next((i for i, part in enumerate(groups) if part.strip().startswith('streak:')), None)

                except ValueError:
                    print("streak: not found in the line")
                    return habits
                try:
                    goal_index = next((i for i, part in enumerate(groups) if part.strip().startswith('goal:')), None)

                except ValueError:
                    print("goal: not found in the line")
                    return habits
                try:
                    log_index = next((i for i, part in enumerate(groups) if part.strip().startswith('log:')), None)

                except ValueError:
                    print("log: not found in the line")
                    return habits

                #parsing id, name, streak and goal
                id = int(groups[id_index].strip().split(': ')[1])
                habit_name = groups[habit_index].strip().split(': ')[1]
                current_streak = int(groups[streak_index].strip().split(': ')[1])
                goal = int(groups[goal_index].strip().split(': ')[1])

                #parsing log of dates
                date_log = groups[log_index].strip().split(': ')[1].strip('[]')
                if date_log:
                    log = [date.fromisoformat(d.strip().strip("'")) for d in date_log.split(',')]
                else:
                    log = []

                habit = {
                    'id': id,
                    'habit_name': habit_name,
                    'goal': goal,
                    'current_streak': current_streak,
                    'log': log
                }
                habits.append(habit)

        print(f"Habits successfully loaded from {filename}")
        return habits
    except FileNotFoundError:
        print("No habits file found. Starting with an empty list.")
        return []
    except Exception as e:
        print(f"Error loading from file: {e}")
        return []

if __name__ == "__main__":
    main()
