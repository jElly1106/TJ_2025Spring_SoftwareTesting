def calendar_problem(year: int, month: int, day: int) -> str:
    if year < 1900 or year > 2100:
        return "年份数值越界"
    if month <= 0 or month > 12:
        return "月份数值越界"

    month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    is_leap = 0

    if year % 400 == 0:
        is_leap = 1
    elif year % 100 != 0 and year % 4 == 0:
        is_leap = 1

    month_days[1] += is_leap
    max_days = month_days[month - 1]

    if day <= 0 or day > max_days:
        return "日期数值越界"

    result = [year, month, day + 1]

    if day == max_days:
        result[2] = 1
        result[1] += 1

    if result[1] > 12:
        result[1] = 1
        result[0] += 1

    return f"{result[0]}/{result[1]}/{result[2]}"


