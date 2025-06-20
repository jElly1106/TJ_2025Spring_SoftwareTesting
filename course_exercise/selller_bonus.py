def calculate_commission(sales_amount, leave_days, cash_arrival_percent):
    """
    计算销售员佣金

    参数:
    - sales_amount: 年销售额（单位 W RMB）
    - leave_days: 请假天数（应在 0 到 366 之间）
    - cash_arrival_percent: 现金到账百分比（0 到 100）

    返回:
    - 佣金金额（float）
    """

    if not isinstance(sales_amount, (int, float)) or sales_amount < 0:
        return "销售额必须为非负数"
    if not isinstance(leave_days, int) or not (0 <= leave_days <= 366):
        return  "请假天数必须为整数，且在 0 到 366 之间"
    if not isinstance(cash_arrival_percent, (int, float)) or not (0 <= cash_arrival_percent <= 100):
        return  "现金到账比例必须为 0 到 100 之间的数"

    if sales_amount > 200 and leave_days <= 10:
        if cash_arrival_percent >= 60:
            commission_factor = 7
        else:
            return 0.0
    else:
        if cash_arrival_percent <= 85:
            commission_factor = 6
        else:
            commission_factor = 5
    commission = sales_amount / commission_factor
    return round(commission, 2)
