def telecom_system(calling_time, count):
    if calling_time < 0 or calling_time > 31 * 24 * 60:
        return "通话时长数值越界"
    if count < 0 or count > 11:
        return "未按时缴费次数越界"

    if calling_time > 0 and calling_time <= 60:
        level = 1
    elif calling_time > 60 and calling_time <= 120:
        level = 2
    elif calling_time > 120 and calling_time <= 180:
        level = 3
    elif calling_time > 180 and calling_time <= 300:
        level = 4
    else:
        level = 5

    max_num = [1, 2, 3, 3, 6]

    if count <= max_num[level - 1]:
        return str(round((25 + 0.15 * calling_time * (1 - (level + 1) * 0.005)) * 100) / 100)

    return str(round((25 + 0.15 * calling_time) * 100) / 100)

