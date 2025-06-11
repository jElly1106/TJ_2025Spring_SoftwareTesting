"""
静态数据存储模块
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
    
    "telecom_system": '''def get_level(time):
    if time > 0 and time <= 60:
        return 1
    
    if time > 60 and time <= 120:
        return 2
    
    if time > 120 and time <= 180:
        return 3
    
    if time > 180 and time <= 300:
        return 4
    
    return 5

def telecom_system(calling_time, count):
    if calling_time < 0 or calling_time > 31 * 24 * 60:
        return "通话时长数值越界"
    
    if count < 0 or count > 11:
        return "未按时缴费次数越界"
    
    max_num = [1, 2, 3, 3, 6]
    level = get_level(calling_time)
    
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

    return f"{result[0]}/{result[1]}/{result[2]}"'''
}

# 测试用例数据结构 - 按函数名分组
TEST_CASES = {
    "triangle_judge": {
        "function_name": "triangle_judge",
        "description": "三角形判断函数测试用例",
        "test_methods": {
            "boundary_basic": {
                "name": "基本边界值测试",
                "description": "测试边界值：1, 2, 199, 200，按照边界值测试原则设计",
                "cases": [
                    # 基本边界值测试：固定两个变量为正常值，一个变量取边界值
                    # 正常值选择100（在1-200范围内的中间值）
                    
                    # 变量a的边界值测试（b=100, c=100）
                    {"input": [1, 100, 100], "expected": "该三角形是等腰三角形"},      # a=min
                    {"input": [2, 100, 100], "expected": "该三角形是等腰三角形"},      # a=min+1
                    {"input": [199, 100, 100], "expected": "该三角形是等腰三角形"},    # a=max-1
                    {"input": [200, 100, 100], "expected": "所给三边数据不能构成三角形"}, # a=max, 200>100+100
                    
                    # 变量b的边界值测试（a=100, c=100）
                    {"input": [100, 1, 100], "expected": "该三角形是等腰三角形"},      # b=min
                    {"input": [100, 2, 100], "expected": "该三角形是等腰三角形"},      # b=min+1
                    {"input": [100, 199, 100], "expected": "该三角形是等腰三角形"},    # b=max-1
                    {"input": [100, 200, 100], "expected": "所给三边数据不能构成三角形"}, # b=max, 200>100+100
                    
                    # 变量c的边界值测试（a=100, b=100）
                    {"input": [100, 100, 1], "expected": "该三角形是等腰三角形"},      # c=min
                    {"input": [100, 100, 2], "expected": "该三角形是等腰三角形"},      # c=min+1
                    {"input": [100, 100, 199], "expected": "该三角形是等腰三角形"},    # c=max-1
                    {"input": [100, 100, 200], "expected": "所给三边数据不能构成三角形"}, # c=max, 200>100+100
                    
                    # 正常值测试
                    {"input": [100, 100, 100], "expected": "该三角形是等边三角形"},
                ]
            },
            
            "boundary_robust": {
                "name": "健壮边界值测试",
                "description": "测试边界值及其相邻的无效值：0, 1, 2, 199, 200, 201",
                "cases": [
                    # 无效边界值（越界）
                    {"input": [0, 100, 100], "expected": "边长数值越界"},
                    {"input": [201, 100, 100], "expected": "边长数值越界"},
                    {"input": [100, 0, 100], "expected": "边长数值越界"},
                    {"input": [100, 201, 100], "expected": "边长数值越界"},
                    {"input": [100, 100, 0], "expected": "边长数值越界"},
                    {"input": [100, 100, 201], "expected": "边长数值越界"},
                    
                    # 有效边界值
                    {"input": [1, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [2, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [199, 100, 100], "expected": "该三角形是等腰三角形"},
                    {"input": [200, 100, 100], "expected": "所给三边数据不能构成三角形"},
                    
                    # 边界值的特殊情况
                    {"input": [1, 1, 1], "expected": "该三角形是等边三角形"},
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},
                ]
            },
            
            "equivalent_weak": {
                "name": "弱一般等价类测试",
                "description": "每个等价类选择一个代表值进行测试",
                "cases": [
                    # 有效等价类
                    {"input": [100, 100, 100], "expected": "该三角形是等边三角形"},  # 等边三角形
                    {"input": [100, 100, 50], "expected": "该三角形是等腰三角形"},   # 等腰三角形
                    {"input": [30, 40, 60], "expected": "该三角形是普通三角形"},     # 普通三角形
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},    # 不能构成三角形
                    
                    # 无效等价类（选择一个代表）
                    {"input": [0, 100, 100], "expected": "边长数值越界"},           # 越界值
                ]
            },
            
            "equivalent_strong": {
                "name": "强一般等价类测试",
                "description": "所有等价类的笛卡尔积组合",
                "cases": [
                    # 有效输入的所有组合
                    {"input": [50, 50, 50], "expected": "该三角形是等边三角形"},     # 等边
                    {"input": [50, 50, 30], "expected": "该三角形是等腰三角形"},     # 等腰(a=b)
                    {"input": [50, 30, 50], "expected": "该三角形是等腰三角形"},     # 等腰(a=c)
                    {"input": [30, 50, 50], "expected": "该三角形是等腰三角形"},     # 等腰(b=c)
                    {"input": [30, 40, 60], "expected": "该三角形是普通三角形"},     # 普通
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},   # 不能构成
                    {"input": [1, 10, 20], "expected": "所给三边数据不能构成三角形"}, # 不能构成
                    {"input": [10, 1, 20], "expected": "所给三边数据不能构成三角形"}, # 不能构成
                    {"input": [10, 20, 1], "expected": "所给三边数据不能构成三角形"}, # 不能构成
                ]
            },
            
            "equivalent_weak_robust": {
                "name": "弱健壮等价类测试",
                "description": "包含无效等价类的弱等价类测试",
                "cases": [
                    # 有效等价类
                    {"input": [100, 100, 100], "expected": "该三角形是等边三角形"},
                    {"input": [100, 100, 50], "expected": "该三角形是等腰三角形"},
                    {"input": [30, 40, 60], "expected": "该三角形是普通三角形"},
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},
                    
                    # 无效等价类
                    {"input": [0, 100, 100], "expected": "边长数值越界"},          # a <= 0
                    {"input": [-5, 100, 100], "expected": "边长数值越界"},         # a < 0
                    {"input": [201, 100, 100], "expected": "边长数值越界"},        # a > 200
                    {"input": [300, 100, 100], "expected": "边长数值越界"},        # a >> 200
                    {"input": [100, 0, 100], "expected": "边长数值越界"},          # b <= 0
                    {"input": [100, -3, 100], "expected": "边长数值越界"},         # b < 0
                    {"input": [100, 250, 100], "expected": "边长数值越界"},        # b > 200
                    {"input": [100, 100, 0], "expected": "边长数值越界"},          # c <= 0
                    {"input": [100, 100, -1], "expected": "边长数值越界"},         # c < 0
                    {"input": [100, 100, 500], "expected": "边长数值越界"},        # c > 200
                ]
            },
            
            "equivalent_strong_robust": {
                "name": "强健壮等价类测试",
                "description": "所有有效和无效等价类的笛卡尔积组合",
                "cases": [
                    # 有效输入组合
                    {"input": [50, 50, 50], "expected": "该三角形是等边三角形"},
                    {"input": [50, 50, 30], "expected": "该三角形是等腰三角形"},
                    {"input": [30, 40, 60], "expected": "该三角形是普通三角形"},
                    {"input": [1, 1, 3], "expected": "所给三边数据不能构成三角形"},
                    
                    # 一个参数无效的组合
                    {"input": [0, 50, 50], "expected": "边长数值越界"},
                    {"input": [201, 50, 50], "expected": "边长数值越界"},
                    {"input": [50, 0, 50], "expected": "边长数值越界"},
                    {"input": [50, 201, 50], "expected": "边长数值越界"},
                    {"input": [50, 50, 0], "expected": "边长数值越界"},
                    {"input": [50, 50, 201], "expected": "边长数值越界"},
                    
                    # 两个参数无效的组合
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
                    
                    # 三个参数都无效的组合
                    {"input": [0, 0, 0], "expected": "边长数值越界"},
                    {"input": [0, 0, 201], "expected": "边长数值越界"},
                    {"input": [0, 201, 0], "expected": "边长数值越界"},
                    {"input": [0, 201, 201], "expected": "边长数值越界"},
                    {"input": [201, 0, 0], "expected": "边长数值越界"},
                    {"input": [201, 0, 201], "expected": "边长数值越界"},
                    {"input": [201, 201, 0], "expected": "边长数值越界"},
                    {"input": [201, 201, 201], "expected": "边长数值越界"},
                ]
            }
        }
    }
    # 可以在这里添加其他函数的测试用例
    # "computer_selling": {
    #     "function_name": "computer_selling",
    #     "description": "计算机销售函数测试用例",
    #     "test_methods": {
    #         "boundary_basic": {...},
    #         ...
    #     }
    # }
}

# 支持的测试方法列表
SUPPORTED_TEST_METHODS = [
    "boundary_basic", 
    "boundary_robust", 
    "equivalent_weak", 
    "equivalent_strong", 
    "equivalent_weak_robust", 
    "equivalent_strong_robust"
]

# 支持的函数列表
SUPPORTED_FUNCTIONS = list(TEST_CASES.keys())

# 为了向后兼容，保留原来的 TRIANGLE_TEST_CASES
TRIANGLE_TEST_CASES = TEST_CASES["triangle_judge"]["test_methods"]