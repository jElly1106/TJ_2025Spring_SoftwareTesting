import json
import sys
import os
import time
from typing import List, Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from app.data.static_data import TEST_CASES, SUPPORTED_TEST_METHODS, SUPPORTED_FUNCTIONS

def generate_test_cases(code: str, function_name: str, test_method: str) -> Dict[str, Any]:
    """
    通用测试用例生成函数
    
    参数:
    code: 要测试的代码源码
    function_name: 函数名称 ("triangle_judge", "computer_selling", "telecom_system", "calendar_problem")
    test_method: 测试方法 ("boundary_basic", "boundary_robust", "equivalent_weak", 
                "equivalent_strong", "equivalent_weak_robust", "equivalent_strong_robust")
    
    返回:
    包含测试用例和预期结果的JSON格式字典
    """
    
    # 检查函数是否支持
    if function_name not in TEST_CASES:
        return {
            "success": False,
            "message": f"不支持的函数: {function_name}",
            "available_functions": SUPPORTED_FUNCTIONS
        }
    
    function_test_cases = TEST_CASES[function_name]
    
    # 检查测试方法是否支持
    if test_method not in function_test_cases["test_methods"]:
        available_methods = list(function_test_cases["test_methods"].keys())
        return {
            "success": False,
            "message": f"函数{function_name}不支持的测试方法: {test_method}",
            "available_methods": available_methods
        }
    
    selected_test = function_test_cases["test_methods"][test_method]
    
    # 执行测试用例
    test_results = []
    passed_count = 0
    failed_count = 0
    
    try:
        # 动态执行代码
        local_vars = {}
        exec(code, globals(), local_vars)
        
        # 获取要测试的函数
        test_function = local_vars.get(function_name) or globals().get(function_name)
        
        if test_function is None:
            return {
                "success": False,
                "message": f"代码中未找到函数: {function_name}",
                "function_name": function_name
            }
        
        for i, case in enumerate(selected_test["cases"]):
            # 记录开始时间
            start_time = time.perf_counter()
            
            try:
                # 调用测试函数
                if isinstance(case["input"], list):
                    actual = test_function(*case["input"])
                else:
                    actual = test_function(case["input"])
                
                # 记录结束时间
                end_time = time.perf_counter()
                duration = round((end_time - start_time) * 1000, 3)  # 转换为毫秒，保留3位小数
                
                expected = case["expected"]
                is_passed = actual == expected
                
                test_results.append({
                    "ID": i + 1,
                    "Input": case["input"],
                    "Expected": expected,
                    "Actual": actual,
                    "Passed": is_passed,
                    "Duration": f"{duration}ms"
                })
                
                if is_passed:
                    passed_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                # 记录结束时间（即使出错也要记录）
                end_time = time.perf_counter()
                duration = round((end_time - start_time) * 1000, 3)
                
                test_results.append({
                    "ID": i + 1,
                    "Input": case["input"],
                    "Expected": case["expected"],
                    "Actual": f"执行错误: {str(e)}",
                    "Passed": False,
                    "Duration": f"{duration}ms"
                })
                failed_count += 1
                
    except Exception as e:
        return {
            "success": False,
            "message": f"代码执行错误: {str(e)}",
            "function_name": function_name,
            "test_method": test_method
        }
    
    total_cases = len(selected_test["cases"])
    pass_rate = round((passed_count / total_cases) * 100, 2) if total_cases > 0 else 0
    
    return {
        "success": True,
        "function_name": function_name,
        "test_method": test_method,
        "test_name": selected_test["name"],
        "description": selected_test["description"],
        "summary": {
            "total_cases": total_cases,
            "passed_cases": passed_count,
            "failed_cases": failed_count,
            "pass_rate": f"{pass_rate}%"
        },
        "test_results": test_results
    }

def get_test_results_json(code: str, function_name: str, test_method: str) -> str:
    """
    获取JSON格式的测试结果字符串
    
    参数:
    code: 要测试的代码源码
    function_name: 函数名称
    test_method: 测试方法
    
    返回:
    JSON格式的字符串
    """
    result = generate_test_cases(code, function_name, test_method)
    return json.dumps(result, ensure_ascii=False, indent=2)

# 为了向后兼容，保留原函数名
def generate_triangle_test_cases(code: str, test_method: str) -> Dict[str, Any]:
    """
    三角形测试用例生成函数（向后兼容）
    """
    return generate_test_cases(code, "triangle_judge", test_method)

# 测试函数
if __name__ == "__main__":
    from app.data.static_data import HOMEWORK_CODES
    
    # 测试triangle_judge函数
    function_name = "triangle_judge"
    sample_code = HOMEWORK_CODES[function_name]
    
    print(f"测试函数: {function_name}")
    print("=" * 50)
    
    # 测试基本边界值方法
    test_method = "boundary_basic"
    result = generate_test_cases(sample_code, function_name, test_method)
    
    if result["success"]:
        print(f"\n测试方法: {result['test_name']}")
        print(f"描述: {result['description']}")
        print(f"总用例数: {result['summary']['total_cases']}")
        print(f"通过用例数: {result['summary']['passed_cases']}")
        print(f"失败用例数: {result['summary']['failed_cases']}")
        print(f"通过率: {result['summary']['pass_rate']}")
        
        print("\n详细测试结果:")
        print("-" * 80)
        print(f"{'ID':<3} {'Input':<20} {'Expected':<30} {'Actual':<30} {'Passed':<7} {'Duration':<10}")
        print("-" * 80)
        
        for test_case in result["test_results"]:
            input_str = str(test_case["Input"])[:18] + ".." if len(str(test_case["Input"])) > 20 else str(test_case["Input"])
            expected_str = str(test_case["Expected"])[:28] + ".." if len(str(test_case["Expected"])) > 30 else str(test_case["Expected"])
            actual_str = str(test_case["Actual"])[:28] + ".." if len(str(test_case["Actual"])) > 30 else str(test_case["Actual"])
            
            print(f"{test_case['ID']:<3} {input_str:<20} {expected_str:<30} {actual_str:<30} {test_case['Passed']:<7} {test_case['Duration']:<10}")
        
        # 输出JSON格式
        print("\n" + "=" * 50)
        print("JSON格式输出:")
        print("=" * 50)
        print(get_test_results_json(sample_code, function_name, test_method))
        
    else:
        print(f"测试失败: {result['message']}")