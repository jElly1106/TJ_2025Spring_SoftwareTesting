"""
静态数据存储模块（重新计算后）
包含作业代码和测试用例的静态数据
"""

# 作业代码映射
HOMEWORK_CODES = {
    "triangle_judge": '''def triangle_judge(a: int, b: int, c: int) -> str:
    if a <= 0 or b <= 0 or c <= 0 or a > 200 or b > 200 or c > 200:
        return "边长数值越界"

    if a + b > c and a + c > b and b + c > a:
        if a == b == c:
            return "该三角形是等边三角形"
        if a == b or a == c or b == c:
            return "该三角形是等腰三角形"
        return "该三角形是普通三角形"

    return "所给三边数据不能构成三角形"''',

    "computer_selling": '''def computer_selling(host, monitor, peripheral):
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
    
    return str(total_sales * 0.2)''',

    "telecom_system": '''def telecom_system(calling_time, count):
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
    
    return str(round((25 + 0.15 * calling_time) * 100) / 100)''',

    "calendar_problem": '''def calendar_problem(year: int, month: int, day: int) -> str:
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

    return f"{result[0]}/{result[1]}/{result[2]}"''',

    "seller_bonus":'''def seller_bonus(sales_amount, leave_days, cash_arrival_percent):
    if not isinstance(sales_amount, (int, float)) or sales_amount < 0:
        raise ValueError("销售额必须为非负数")
    if not isinstance(leave_days, int) or not (0 <= leave_days <= 366):
        raise ValueError("请假天数必须为整数，且在 0 到 366 之间")
    if not isinstance(cash_arrival_percent, (int, float)) or not (0 <= cash_arrival_percent <= 100):
        raise ValueError("现金到账比例必须为 0 到 100 之间的数")

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
    return round(commission, 2)'''

}

# 测试用例数据结构 - 按函数名分组（重新计算后）
TEST_CASES = {
    "triangle_judge": {
        "function_name": "triangle_judge",
        "description": "三角形判断函数测试用例",
        "test_methods": {
            "boundary_basic": {
                "name": "基本边界值测试",
                "description": "测试边界值：1, 2, 199, 200，按照边界值测试原则设计",
                "cases": [
                    {"input": [1, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [2, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [199, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [200, 100, 100], "expected": "所给三边数据不能构成三角形"},
                    {"input": [100, 1, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [100, 2, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [100, 199, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [100, 200, 100], "expected": "所给三边数据不能构成三角形"},
                    {"input": [100, 100, 1], "expected": "该三角形是等腰三角形"},
                    {"input": [100, 100, 2], "expected": "该三角形是等腰三角形"},
                    {"input": [100, 100, 199], "expected": "该三角形是等腰三角形"},
                    {"input": [100, 100, 200], "expected": "所给三边数据不能构成三角形"},
                    {"input": [100, 100, 100], "expected": "该三角形是等边三角形"},
                ]
            },

            "boundary_robust": {
                "name": "健壮边界值测试",
                "description": "测试边界值及其相邻的无效值：0, 1, 2, 199, 200, 201",
                "cases": [
                    {"input": [0, 100, 100], "expected": "边长数值越界"},
                    {"input": [201, 100, 100], "expected": "边长数值越界"},
                    {"input": [100, 0, 100], "expected": "边长数值越界"},
                    {"input": [100, 201, 100], "expected": "边长数值越界"},
                    {"input": [100, 100, 0], "expected": "边长数值越界"},
                    {"input": [100, 100, 201], "expected": "边长数值越界"},
                    {"input": [1, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [2, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [199, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [200, 100, 100], "expected": "所给三边数据不能构成三角形"},
                    {"input": [1, 1, 1], "expected": "该三角形是等边三角形"},
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},
                ]
            },

            "equivalent_weak": {
                "name": "弱一般等价类测试",
                "description": "每个等价类选择一个代表值进行测试",
                "cases": [
                    {"input": [100, 100, 100], "expected": "该三角形是等边三角形"},
                    {"input": [100, 100, 50], "expected": "该三角形是等腰三角形"},
                    {"input": [30, 40, 60], "expected": "该三角形是普通三角形"},
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},
                    {"input": [0, 100, 100], "expected": "边长数值越界"},
                ]
            },

            "equivalent_strong": {
                "name": "强一般等价类测试",
                "description": "所有等价类的笛卡尔积组合",
                "cases": [
                    {"input": [50, 50, 50], "expected": "该三角形是等边三角形"},
                    {"input": [50, 50, 30], "expected": "该三角形是等腰三角形"},
                    {"input": [50, 30, 50], "expected": "该三角形是等腰三角形"},
                    {"input": [30, 50, 50], "expected": "该三角形是等腰三角形"},
                    {"input": [30, 40, 60], "expected": "该三角形是普通三角形"},
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},
                    {"input": [1, 10, 20], "expected": "所给三边数据不能构成三角形"},
                    {"input": [10, 1, 20], "expected": "所给三边数据不能构成三角形"},
                    {"input": [10, 20, 1], "expected": "所给三边数据不能构成三角形"},
                ]
            },

            "equivalent_weak_robust": {
                "name": "弱健壮等价类测试",
                "description": "包含无效等价类的弱等价类测试",
                "cases": [
                    {"input": [100, 100, 100], "expected": "该三角形是等边三角形"},
                    {"input": [100, 100, 50], "expected": "该三角形是等腰三角形"},
                    {"input": [30, 40, 60], "expected": "该三角形是普通三角形"},
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},
                    {"input": [0, 100, 100], "expected": "边长数值越界"},
                    {"input": [-5, 100, 100], "expected": "边长数值越界"},
                    {"input": [201, 100, 100], "expected": "边长数值越界"},
                    {"input": [300, 100, 100], "expected": "边长数值越界"},
                    {"input": [100, 0, 100], "expected": "边长数值越界"},
                    {"input": [100, -3, 100], "expected": "边长数值越界"},
                    {"input": [100, 250, 100], "expected": "边长数值越界"},
                    {"input": [100, 100, 0], "expected": "边长数值越界"},
                    {"input": [100, 100, -1], "expected": "边长数值越界"},
                    {"input": [100, 100, 500], "expected": "边长数值越界"},
                ]
            },

            "equivalent_strong_robust": {
                "name": "强健壮等价类测试",
                "description": "所有有效和无效等价类的笛卡尔积组合",
                "cases": [
                    {"input": [50, 50, 50], "expected": "该三角形是等边三角形"},
                    {"input": [50, 50, 30], "expected": "该三角形是等腰三角形"},
                    {"input": [30, 40, 60], "expected": "该三角形是普通三角形"},
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},
                    {"input": [0, 50, 50], "expected": "边长数值越界"},
                    {"input": [201, 50, 50], "expected": "边长数值越界"},
                    {"input": [50, 0, 50], "expected": "边长数值越界"},
                    {"input": [50, 201, 50], "expected": "边长数值越界"},
                    {"input": [50, 50, 0], "expected": "边长数值越界"},
                    {"input": [50, 50, 201], "expected": "边长数值越界"},
                    {"input": [0, 0, 50], "expected": "边长数值越界"},
                    {"input": [0, 201, 50], "expected": "边长数值越界"},
                    {"input": [201, 0, 50], "expected": "边长数值越界"},
                    {"input": [201, 201, 50], "expected": "边长数值越界"},
                    {"input": [0, 50, 0], "expected": "边长数值越界"},
                    {"input": [0, 50, 201], "expected": "边长数值越界"},
                    {"input": [201, 50, 0], "expected": "边长数值越界"},
                    {"input": [201, 50, 201], "expected": "边长数值越界"},
                    {"input": [50, 0, 0], "expected": "边长数值越界"},
                    {"input": [50, 0, 201], "expected": "边长数值越界"},
                    {"input": [50, 201, 0], "expected": "边长数值越界"},
                    {"input": [50, 201, 201], "expected": "边长数值越界"},
                    {"input": [0, 0, 0], "expected": "边长数值越界"},
                    {"input": [0, 0, 201], "expected": "边长数值越界"},
                    {"input": [0, 201, 0], "expected": "边长数值越界"},
                    {"input": [0, 201, 201], "expected": "边长数值越界"},
                    {"input": [201, 0, 0], "expected": "边长数值越界"},
                    {"input": [201, 0, 201], "expected": "边长数值越界"},
                    {"input": [201, 201, 0], "expected": "边长数值越界"},
                    {"input": [201, 201, 201], "expected": "边长数值越界"},
                ]
            },

        }
    },
    "computer_selling": {
        "function_name": "computer_selling",
        "description": "计算机销售函数测试用例",
        "test_methods": {
            "boundary_basic": {
                "name": "基本边界值测试",
                "description": "测试主机[1-70]、显示器[1-80]、外设[1-90]的边界值",
                "cases": [
                    {"input": [1, 40, 45], "expected": "650.0"},
                    {"input": [2, 40, 45], "expected": "655.0"},
                    {"input": [69, 40, 45], "expected": "990.0"},
                    {"input": [70, 40, 45], "expected": "995.0"},
                    {"input": [35, 1, 45], "expected": "586.0"},
                    {"input": [35, 2, 45], "expected": "592.0"},
                    {"input": [35, 79, 45], "expected": "1054.0"},
                    {"input": [35, 80, 45], "expected": "1060.0"},
                    {"input": [35, 40, 1], "expected": "424.0"},
                    {"input": [35, 40, 2], "expected": "433.0"},
                    {"input": [35, 40, 89], "expected": "1216.0"},
                    {"input": [35, 40, 90], "expected": "1225.0"},
                    {"input": [1, 1, 20], "expected": "95.5"},
                    {"input": [1, 1, 21], "expected": "100.0"},
                    {"input": [1, 4, 21], "expected": "163.5"},
                    {"input": [1, 16, 24], "expected": "237.75"},
                    {"input": [1, 17, 24], "expected": "242.25"},
                    {"input": [-1, 0, 0], "expected": "系统开始统计月度销售额"},
                ]
            },

            "boundary_robust": {
                "name": "健壮边界值测试",
                "description": "测试边界值及其相邻的无效值",
                "cases": [
                    {"input": [0, 40, 45], "expected": "数据非法，各部件销售数量不能小于1"},
                    {"input": [71, 40, 45], "expected": "数据非法，主机销售数量不能超过70"},
                    {"input": [-5, 40, 45], "expected": "数据非法，各部件销售数量不能小于1"},
                    {"input": [100, 40, 45], "expected": "数据非法，主机销售数量不能超过70"},
                    {"input": [35, 0, 45], "expected": "数据非法，各部件销售数量不能小于1"},
                    {"input": [35, 81, 45], "expected": "数据非法，显示器销售数量不能超过80"},
                    {"input": [35, -3, 45], "expected": "数据非法，各部件销售数量不能小于1"},
                    {"input": [35, 120, 45], "expected": "数据非法，显示器销售数量不能超过80"},
                    {"input": [35, 40, 0], "expected": "数据非法，各部件销售数量不能小于1"},
                    {"input": [35, 40, 91], "expected": "数据非法，外设销售数量不能超过90"},
                    {"input": [35, 40, -2], "expected": "数据非法，各部件销售数量不能小于1"},
                    {"input": [35, 40, 150], "expected": "数据非法，外设销售数量不能超过90"},
                    {"input": [1, 1, 1], "expected": "10.0"},
                    {"input": [70, 80, 90], "expected": "1640.0"},
                    {"input": [1, 1, 20], "expected": "95.5"},
                    {"input": [8, 8, 8], "expected": "80.0"},
                    {"input": [1, 16, 24], "expected": "237.75"},
                    {"input": [-1, 100, 200], "expected": "系统开始统计月度销售额"},
                ]
            },

        }
    },
    "telecom_system": {
        "function_name": "telecom_system",
        "description": "电信计费系统函数测试用例",
        "test_methods": {
            "boundary_basic": {
                "name": "基本边界值测试",
                "description": "测试通话时长[0-44640]、未按时缴费次数[0-11]的边界值",
                "cases": [
                    {"input": [0, 5], "expected": "25.0"},
                    {"input": [1, 5], "expected": "25.15"},
                    {"input": [44639, 5], "expected": "6519.97"},
                    {"input": [44640, 5], "expected": "6520.12"},
                    {"input": [150, 0], "expected": "47.05"},
                    {"input": [150, 1], "expected": "47.05"},
                    {"input": [150, 10], "expected": "47.5"},
                    {"input": [150, 11], "expected": "47.5"},
                    {"input": [1, 1], "expected": "25.15"},
                    {"input": [60, 1], "expected": "33.91"},
                    {"input": [61, 1], "expected": "34.01"},
                    {"input": [120, 1], "expected": "42.73"},
                    {"input": [121, 2], "expected": "42.79"},
                    {"input": [180, 3], "expected": "51.46"},
                    {"input": [181, 3], "expected": "51.47"},
                    {"input": [300, 3], "expected": "68.88"},
                    {"input": [301, 6], "expected": "68.8"},
                ]
            },

            "boundary_robust": {
                "name": "健壮边界值测试",
                "description": "测试边界值及其相邻的无效值",
                "cases": [
                    {"input": [-1, 5], "expected": "通话时长数值越界"},
                    {"input": [44641, 5], "expected": "通话时长数值越界"},
                    {"input": [-100, 5], "expected": "通话时长数值越界"},
                    {"input": [50000, 5], "expected": "通话时长数值越界"},
                    {"input": [150, -1], "expected": "未按时缴费次数越界"},
                    {"input": [150, 12], "expected": "未按时缴费次数越界"},
                    {"input": [150, -5], "expected": "未按时缴费次数越界"},
                    {"input": [150, 20], "expected": "未按时缴费次数越界"},
                    {"input": [0, 0], "expected": "25.0"},
                    {"input": [44640, 11], "expected": "6721.0"},
                    {"input": [1, 1], "expected": "25.15"},
                    {"input": [60, 1], "expected": "33.91"},
                    {"input": [300, 3], "expected": "68.88"},
                ]
            },

            "equivalent_weak": {
                "name": "弱一般等价类测试",
                "description": "每个等价类选择一个代表值进行测试",
                "cases": [
                    {"input": [30, 1], "expected": "29.46"},
                    {"input": [90, 2], "expected": "38.3"},
                    {"input": [150, 3], "expected": "47.05"},
                    {"input": [240, 3], "expected": "60.1"},
                    {"input": [400, 6], "expected": "83.2"},
                    {"input": [100, 0], "expected": "39.78"},
                    {"input": [100, 5], "expected": "40.0"},
                    {"input": [-10, 5], "expected": "通话时长数值越界"},
                    {"input": [100, -2], "expected": "未按时缴费次数越界"},
                ]
            },

            "equivalent_strong": {
                "name": "强一般等价类测试",
                "description": "所有等价类的笛卡尔积组合",
                "cases": [
                    {"input": [30, 0], "expected": "29.46"},
                    {"input": [30, 1], "expected": "29.46"},
                    {"input": [30, 2], "expected": "29.5"},
                    {"input": [90, 1], "expected": "38.3"},
                    {"input": [90, 2], "expected": "38.3"},
                    {"input": [90, 3], "expected": "38.5"},
                    {"input": [150, 2], "expected": "47.05"},
                    {"input": [150, 3], "expected": "47.05"},
                    {"input": [150, 4], "expected": "47.5"},
                    {"input": [240, 2], "expected": "60.1"},
                    {"input": [240, 3], "expected": "60.1"},
                    {"input": [240, 4], "expected": "61.0"},
                    {"input": [400, 5], "expected": "83.2"},
                    {"input": [400, 6], "expected": "83.2"},
                    {"input": [400, 7], "expected": "85.0"},
                    {"input": [0, 0], "expected": "25.0"},
                    {"input": [0, 11], "expected": "25.0"},
                ]
            },

            "equivalent_weak_robust": {
                "name": "弱健壮等价类测试",
                "description": "包含无效等价类的弱等价类测试",
                "cases": [
                    {"input": [30, 1], "expected": "29.46"},
                    {"input": [90, 2], "expected": "38.3"},
                    {"input": [150, 3], "expected": "47.05"},
                    {"input": [240, 3], "expected": "60.1"},
                    {"input": [400, 6], "expected": "83.2"},
                    {"input": [0, 0], "expected": "25.0"},
                    {"input": [-50, 5], "expected": "通话时长数值越界"},
                    {"input": [50000, 5], "expected": "通话时长数值越界"},
                    {"input": [100, -3], "expected": "未按时缴费次数越界"},
                    {"input": [100, 15], "expected": "未按时缴费次数越界"},
                ]
            },

            "equivalent_strong_robust": {
                "name": "强健壮等价类测试",
                "description": "所有有效和无效等价类的笛卡尔积组合",
                "cases": [
                    {"input": [30, 1], "expected": "29.46"},
                    {"input": [150, 3], "expected": "47.05"},
                    {"input": [400, 6], "expected": "83.2"},
                    {"input": [90, 3], "expected": "38.5"},
                    {"input": [240, 4], "expected": "61.0"},
                    {"input": [0, 0], "expected": "25.0"},
                    {"input": [-10, 5], "expected": "通话时长数值越界"},
                    {"input": [50000, 5], "expected": "通话时长数值越界"},
                    {"input": [100, -1], "expected": "未按时缴费次数越界"},
                    {"input": [100, 15], "expected": "未按时缴费次数越界"},
                    {"input": [-10, -1], "expected": "通话时长数值越界"},
                    {"input": [-10, 15], "expected": "通话时长数值越界"},
                    {"input": [50000, -1], "expected": "通话时长数值越界"},
                    {"input": [50000, 15], "expected": "通话时长数值越界"},
                ]
            },

            "decision_table": {
                "name": "决策表测试",
                "description": "基于决策表的测试用例设计",
                "cases": [
                    {"input": [-100, 5], "expected": "通话时长数值越界"},
                    {"input": [50000, 5], "expected": "通话时长数值越界"},
                    {"input": [100, -1], "expected": "未按时缴费次数越界"},
                    {"input": [100, 15], "expected": "未按时缴费次数越界"},
                    {"input": [30, 0], "expected": "29.46"},
                    {"input": [60, 1], "expected": "33.91"},
                    {"input": [30, 2], "expected": "29.5"},
                    {"input": [90, 1], "expected": "38.3"},
                    {"input": [90, 2], "expected": "38.3"},
                    {"input": [90, 3], "expected": "38.5"},
                    {"input": [150, 2], "expected": "47.05"},
                    {"input": [150, 3], "expected": "47.05"},
                    {"input": [150, 4], "expected": "47.5"},
                    {"input": [240, 2], "expected": "60.1"},
                    {"input": [240, 3], "expected": "60.1"},
                    {"input": [240, 4], "expected": "61.0"},
                    {"input": [400, 5], "expected": "83.2"},
                    {"input": [400, 6], "expected": "83.2"},
                    {"input": [400, 7], "expected": "85.0"},
                    {"input": [0, 0], "expected": "25.0"},
                    {"input": [0, 11], "expected": "25.0"},
                    {"input": [1, 0], "expected": "25.15"},
                    {"input": [44640, 11], "expected": "6721.0"},
                    {"input": [60, 1], "expected": "33.91"},
                    {"input": [61, 2], "expected": "34.01"},
                    {"input": [120, 2], "expected": "42.73"},
                    {"input": [121, 3], "expected": "42.79"},
                    {"input": [180, 3], "expected": "51.46"},
                    {"input": [181, 3], "expected": "51.47"},
                    {"input": [300, 3], "expected": "68.88"},
                    {"input": [301, 6], "expected": "68.8"},
                ]
            },

        }
    },
    "calendar_problem": {
        "function_name": "calendar_problem",
        "description": "日历问题函数测试用例",
        "test_methods": {
            "boundary_basic": {
                "name": "基本边界值测试",
                "description": "测试年份[1900-2100]、月份[1-12]、日期边界值",
                "cases": [
                    {"input": [1900, 6, 15], "expected": "1900/6/16"},
                    {"input": [1901, 6, 15], "expected": "1901/6/16"},
                    {"input": [2099, 6, 15], "expected": "2099/6/16"},
                    {"input": [2100, 6, 15], "expected": "2100/6/16"},
                    {"input": [2000, 1, 15], "expected": "2000/1/16"},
                    {"input": [2000, 2, 15], "expected": "2000/2/16"},
                    {"input": [2000, 11, 15], "expected": "2000/11/16"},
                    {"input": [2000, 12, 15], "expected": "2000/12/16"},
                    {"input": [2000, 6, 1], "expected": "2000/6/2"},
                    {"input": [2000, 6, 2], "expected": "2000/6/3"},
                    {"input": [2000, 6, 29], "expected": "2000/6/30"},
                    {"input": [2000, 6, 30], "expected": "2000/7/1"},
                    {"input": [2000, 1, 31], "expected": "2000/2/1"},
                    {"input": [2000, 12, 31], "expected": "2001/1/1"},
                ]
            },

            "boundary_robust": {
                "name": "健壮边界值测试",
                "description": "测试边界值及其相邻的无效值",
                "cases": [
                    {"input": [1899, 6, 15], "expected": "年份数值越界"},
                    {"input": [2101, 6, 15], "expected": "年份数值越界"},
                    {"input": [2000, 0, 15], "expected": "月份数值越界"},
                    {"input": [2000, 13, 15], "expected": "月份数值越界"},
                    {"input": [2000, -1, 15], "expected": "月份数值越界"},
                    {"input": [2000, 6, 0], "expected": "日期数值越界"},
                    {"input": [2000, 6, 31], "expected": "日期数值越界"},
                    {"input": [2000, 2, 30], "expected": "日期数值越界"},
                    {"input": [1900, 2, 29], "expected": "日期数值越界"},
                    {"input": [1900, 1, 1], "expected": "1900/1/2"},
                    {"input": [2100, 12, 31], "expected": "2101/1/1"},
                    {"input": [2000, 2, 29], "expected": "2000/3/1"},
                    {"input": [2004, 2, 29], "expected": "2004/3/1"},
                ]
            },

            "equivalent_weak": {
                "name": "弱一般等价类测试",
                "description": "每个等价类选择一个代表值进行测试",
                "cases": [
                    {"input": [2000, 6, 15], "expected": "2000/6/16"},
                    {"input": [2000, 2, 28], "expected": "2000/2/29"},
                    {"input": [2000, 2, 29], "expected": "2000/3/1"},
                    {"input": [2000, 1, 31], "expected": "2000/2/1"},
                    {"input": [2000, 4, 30], "expected": "2000/5/1"},
                    {"input": [2000, 12, 31], "expected": "2001/1/1"},
                    {"input": [1800, 6, 15], "expected": "年份数值越界"},
                    {"input": [2000, 15, 15], "expected": "月份数值越界"},
                    {"input": [2000, 6, 35], "expected": "日期数值越界"},
                ]
            },

            "equivalent_strong": {
                "name": "强一般等价类测试",
                "description": "所有等价类的笛卡尔积组合",
                "cases": [
                    {"input": [2000, 6, 15], "expected": "2000/6/16"},
                    {"input": [2001, 6, 15], "expected": "2001/6/16"},
                    {"input": [2000, 2, 28], "expected": "2000/2/29"},
                    {"input": [2001, 2, 28], "expected": "2001/3/1"},
                    {"input": [2000, 1, 31], "expected": "2000/2/1"},
                    {"input": [2000, 4, 30], "expected": "2000/5/1"},
                    {"input": [2000, 2, 29], "expected": "2000/3/1"},
                    {"input": [2000, 6, 1], "expected": "2000/6/2"},
                    {"input": [2000, 6, 15], "expected": "2000/6/16"},
                    {"input": [2000, 6, 30], "expected": "2000/7/1"},
                    {"input": [2000, 12, 31], "expected": "2001/1/1"},
                ]
            },

            "equivalent_weak_robust": {
                "name": "弱健壮等价类测试",
                "description": "包含无效等价类的弱等价类测试",
                "cases": [
                    {"input": [2000, 6, 15], "expected": "2000/6/16"},
                    {"input": [2000, 2, 29], "expected": "2000/3/1"},
                    {"input": [2000, 12, 31], "expected": "2001/1/1"},
                    {"input": [1800, 6, 15], "expected": "年份数值越界"},
                    {"input": [2200, 6, 15], "expected": "年份数值越界"},
                    {"input": [2000, 0, 15], "expected": "月份数值越界"},
                    {"input": [2000, 13, 15], "expected": "月份数值越界"},
                    {"input": [2000, 6, 0], "expected": "日期数值越界"},
                    {"input": [2000, 6, 32], "expected": "日期数值越界"},
                    {"input": [1900, 2, 29], "expected": "日期数值越界"},
                ]
            },

            "equivalent_strong_robust": {
                "name": "强健壮等价类测试",
                "description": "所有有效和无效等价类的笛卡尔积组合",
                "cases": [
                    {"input": [2000, 6, 15], "expected": "2000/6/16"},
                    {"input": [2001, 2, 28], "expected": "2001/3/1"},
                    {"input": [2000, 12, 31], "expected": "2001/1/1"},
                    {"input": [1800, 6, 15], "expected": "年份数值越界"},
                    {"input": [2200, 6, 15], "expected": "年份数值越界"},
                    {"input": [2000, 0, 15], "expected": "月份数值越界"},
                    {"input": [2000, 13, 15], "expected": "月份数值越界"},
                    {"input": [2000, 6, 0], "expected": "日期数值越界"},
                    {"input": [2000, 6, 32], "expected": "日期数值越界"},
                    {"input": [1800, 0, 15], "expected": "年份数值越界"},
                    {"input": [1800, 6, 0], "expected": "年份数值越界"},
                    {"input": [2000, 0, 0], "expected": "月份数值越界"},
                    {"input": [1800, 0, 0], "expected": "年份数值越界"},
                ]
            },

            "decision_table": {
                "name": "决策表测试",
                "description": "基于决策表的测试用例设计",
                "cases": [
                    {"input": [1800, 6, 15], "expected": "年份数值越界"},
                    {"input": [2200, 6, 15], "expected": "年份数值越界"},
                    {"input": [2000, 0, 15], "expected": "月份数值越界"},
                    {"input": [2000, 13, 15], "expected": "月份数值越界"},
                    {"input": [2000, 2, 29], "expected": "2000/3/1"},
                    {"input": [2004, 2, 29], "expected": "2004/3/1"},
                    {"input": [1900, 2, 29], "expected": "日期数值越界"},
                    {"input": [2001, 2, 29], "expected": "日期数值越界"},
                    {"input": [2000, 2, 28], "expected": "2000/2/29"},
                    {"input": [2001, 2, 28], "expected": "2001/3/1"},
                    {"input": [2000, 1, 31], "expected": "2000/2/1"},
                    {"input": [2000, 3, 31], "expected": "2000/4/1"},
                    {"input": [2000, 4, 31], "expected": "日期数值越界"},
                    {"input": [2000, 6, 31], "expected": "日期数值越界"},
                    {"input": [2000, 4, 30], "expected": "2000/5/1"},
                    {"input": [2000, 6, 30], "expected": "2000/7/1"},
                    {"input": [2000, 12, 31], "expected": "2001/1/1"},
                    {"input": [2000, 6, 0], "expected": "日期数值越界"},
                    {"input": [2000, 6, -1], "expected": "日期数值越界"},
                    {"input": [2000, 6, 15], "expected": "2000/6/16"},
                    {"input": [2001, 7, 20], "expected": "2001/7/21"},
                ]
            },

        }
    },
    "seller_bonus": {
    "function_name": "seller_bonus",
        "description": "销售员佣金问题函数测试用例",
        "test_methods": {
            "statement_coverage": {
                "name": "语句覆盖",
                "description": "语句覆盖",
                "cases": [
                    {"input": [700, 6, 90], "expected": 100},
                    {"input": [120, 6, 80], "expected": 20},

                ]
            },
        "judgement_coverage": {
                "name": "判断覆盖",
                "description": "判断覆盖",
                "cases": [
                    {"input": [700, 6, 90], "expected": 100},
                    {"input": [120, 6, 50], "expected": 20},
                    {"input": [100, 6, 90], "expected": 20},
                    {"input": [120, 6, 80], "expected": 20},
                ]
            },
        "condition_coverage": {
                "name": "条件覆盖",
                "description": "条件覆盖",
                "cases": [
                    {"input": [700, 6, 90], "expected": 100},
                    {"input": [120, 6, 50], "expected": 20},
                    {"input": [100, 6, 90], "expected": 20},
                    {"input": [120, 6, 80], "expected": 20},
                    {"input": [120, 20, 50], "expected": 20},
                ]
            },
        "judgement_condition_coverage": {
                "name": "判断—条件覆盖",
                "description": "判断—条件覆盖",
                "cases": [
{"input": [120, 10, 50], "expected": 20},
                ]
            },
        "condition_combination_coverage": {
                "name": "条件组合覆盖",
                "description": "条件组合覆盖",
                "cases": [
{"input": [700, 5, 90], "expected": 100},


{"input": [210, 5, 50], "expected": 0},


{"input": [100, 5, 90], "expected": 20},


{"input": [120, 15, 70], "expected": 20},


{"input": [300, 15, 50], "expected": 50},


{"input": [180, 5, 70], "expected": 30},


{"input": [250, 15, 90], "expected": 50},


{"input": [300, 15, 70], "expected": 50}
                ]
            }

        },
    },
}

# 支持的测试方法列表
SUPPORTED_TEST_METHODS = [
    "boundary_basic",
    "boundary_robust",
    "equivalent_weak",
    "equivalent_strong",
    "equivalent_weak_robust",
    "equivalent_strong_robust",
    "decision_table",
    "statement_coverage",
    "judgement_coverage",
    "condition_coverage",
    "judgement_condition_coverage",
    "condition_combination_coverage"


]

# 支持的函数列表
SUPPORTED_FUNCTIONS = list(TEST_CASES.keys())
