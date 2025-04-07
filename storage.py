from datetime import date

def file_saving(habits, filename='habits_log.txt'):
    try:
        with open(filename, 'w') as file:
            for h in habits:
                log = [d.isoformat() for d in h['log']]
                file.write(f"id: {h['id']}; habit: {h['habit_name']}; streak: {h['current_streak']}; goal: {h['goal']}; log: {log}\n")
        return(f"Habits successfully saved to {filename}")

    except FileNotFoundError:
        print(f"File {filename} doesn't exist")
    except OSError as e:
        print(f"OSError: {e}")
    except Exception as e:
        return(f"Unexpected error: {e}")

def file_loading(filename='habits_log.txt'):
    habits = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                groups = line.strip().split(';')
                id = int(groups[0].strip().split(': ')[1])
                habit_name = groups[1].strip().split(': ')[1]
                current_streak = int(groups[2].strip().split(': ')[1])
                goal = int(groups[3].strip().split(': ')[1])

                date_log = groups[4].strip().split(': ')[1].strip('[]')
                log = [date.fromisoformat(d.strip().strip("'")) for d in date_log.split(',')] if date_log else []

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
