from datetime import datetime

from .interface.console_style import console


def validate_date_input(year_input: str, month_input: str, day_input: str):
    if (
        year_input.strip() != ""
        and month_input.strip() != ""
        and day_input.strip() != ""
    ):
        year = int(year_input)
        month = int(month_input)
        day = int(day_input)
    else:
        console.print("[prompt.invalid]Please enter valid values.")
        return False

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


def create_date(year: str, month: str, day: str):
    if year and month and day:
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
