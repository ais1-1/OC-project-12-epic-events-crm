from datetime import datetime

from .interface.console_style import console


def validate_date_input(year: str, month: str, day: str):

    # Get Max value for a day in given month
    if (
        month == 1
        or month == 3
        or month == 5
        or month == 7
        or month == 8
        or month == 10
        or month == 12
    ):
        max_day_value = 31
    elif month == 4 or month == 6 or month == 9 or month == 11:
        max_day_value = 30
    elif year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        max_day_value = 29
    else:
        max_day_value = 28

    if year < 0 or (year // 100) < 20:
        console.print("[prompt.invalid]Year is invalid")
        return False
    elif month < 1 or month > 12:
        console.print("[prompt.invalid]Month is invalid.")
        return False
    elif day < 1 or day > max_day_value:
        console.print("[prompt.invalid]Day is invalid.")
        return False
    else:
        return True


def validate_time_input(hour: int, minute: int):
    if hour < 0 or hour > 23:
        console.print("[prompt.invalid]Hour is invalid.")
        return False
    elif minute < 0 or minute > 59:
        console.print("[prompt.invalid]Minute is invalid")
        return False
    else:
        return True


def create_date(year: int, month: int, day: int, hour: int = None, minute: int = None):
    year = str(year)
    month = str(month)
    day = str(day)
    if year and month and day and hour and minute:
        hour = str(hour)
        minute = str(minute)
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        if len(hour) == 1:
            hour = "0" + hour
        if len(minute) == 1:
            minute = "0" + minute
        entry = f"{year}-{month}-{day} {hour}:{minute}"
        datetime_object = datetime.strptime(entry, "%Y-%m-%d %H:%M")
        datetime_string = datetime_object.strftime("%Y-%m-%d %H:%M")
        return datetime_string
    elif year and month and day:
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        entry = f"{year}-{month}-{day}"
        date_object = datetime.strptime(entry, "%Y-%m-%d")
        date_string = date_object.strftime("%Y-%m-%d")
        return date_string
    else:
        return None
