from storage import file_loading, file_saving
from habit import add_habit, checkin, generate_report
from utils import valid_date
from datetime import date

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
                habit_counter += 1
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
