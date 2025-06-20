def computer_selling(host, monitor, peripheral):
    if host == -1:
        return "系统开始统计月度销售额"
    if host <= 0 or monitor <= 0 or peripheral <= 0:
        return "数据非法，各部件销售数量不能小于1"

    if host > 70:
        return "数据非法，主机销售数量不能超过70"

    if monitor > 80:
        return "数据非法，显示器销售数量不能超过80"

    if peripheral > 90:
        return "数据非法，外设销售数量不能超过90"

    total_sales = host * 25 + monitor * 30 + peripheral * 45

    if total_sales <= 1000:
        return str(total_sales * 0.1)

    if total_sales <= 1800:
        return str(total_sales * 0.15)

    return str(total_sales * 0.2)


