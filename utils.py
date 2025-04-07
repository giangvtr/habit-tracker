from datetime import date, timedelta

def valid_date(day_str):
    today = date.today()
    try:
        day = date.fromisoformat(day_str)
        if day > today:
            print("Date to be logged cannot be in the future")
            return None
        return day
    except ValueError:
        print("Invalid date format. Please follow YYYY-MM-DD.")
        return None

def calcul_streak(log):
    if not log:
        return 0

    log.sort(reverse=True)
    streak = 1
    last_date = log[0]

    for i in range(1, len(log)):
        if last_date - log[i] == timedelta(days=1):
            streak += 1
            last_date = log[i]
        else:
            break

    return streak