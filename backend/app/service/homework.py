import json
import sys
import os
import time
from typing import List, Dict, Any



from app.static.homework_data import TEST_CASES, SUPPORTED_TEST_METHODS, SUPPORTED_FUNCTIONS

def generate_test_cases(code: str, function_name: str, test_method: str) -> Dict[str, Any]:
    """
    通用测试用例生成函数
    
    参数:
    code: 要测试的代码源码
    function_name: 函数名称 ("triangle_judge", "computer_selling", "telecom_system", "calendar_problem")
    test_method: 测试方法 ("boundary_basic", "boundary_robust", "equivalent_weak", 
                "equivalent_strong", "equivalent_weak_robust", "equivalent_strong_robust", "decision_table")
    
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

# 测试函数
if __name__ == "__main__":
    from app.data.static_data import HOMEWORK_CODES
    
    print("=" * 80)
    print("软件测试工具 - 全面测试报告")
    print("=" * 80)
    
    # 统计信息
    total_functions = 0
    total_methods = 0
    total_cases = 0
    total_passed = 0
    total_failed = 0
    
    # 测试所有支持的函数
    for function_name in SUPPORTED_FUNCTIONS:
        if function_name not in HOMEWORK_CODES:
            print(f"\n警告: 函数 {function_name} 没有对应的代码实现，跳过测试")
            continue
            
        sample_code = HOMEWORK_CODES[function_name]
        total_functions += 1
        
        print(f"\n{'='*60}")
        print(f"测试函数: {function_name}")
        print(f"函数描述: {TEST_CASES[function_name]['description']}")
        print("=" * 60)
        
        # 获取该函数支持的测试方法
        available_methods = list(TEST_CASES[function_name]["test_methods"].keys())
        function_methods = 0
        function_cases = 0
        function_passed = 0
        function_failed = 0
        
        # 测试该函数的所有方法
        for method in available_methods:
            result = generate_test_cases(sample_code, function_name, method)
            function_methods += 1
            total_methods += 1
            
            if result["success"]:
                method_cases = result['summary']['total_cases']
                method_passed = result['summary']['passed_cases']
                method_failed = result['summary']['failed_cases']
                
                function_cases += method_cases
                function_passed += method_passed
                function_failed += method_failed
                
                total_cases += method_cases
                total_passed += method_passed
                total_failed += method_failed
                
                print(f"\n--- {result['test_name']} ---")
                print(f"描述: {result['description']}")
                print(f"总用例数: {method_cases}")
                print(f"通过: {method_passed}, 失败: {method_failed}")
                print(f"通过率: {result['summary']['pass_rate']}")
                
                # 如果有失败的用例，显示失败详情
                failed_cases = [r for r in result['test_results'] if not r['Passed']]
                if failed_cases:
                    print("失败的测试用例:")
                    for case in failed_cases[:3]:  # 只显示前3个失败用例，避免输出过长
                        print(f"  - 用例{case['ID']}: {case['Input']} -> 期望: '{case['Expected']}', 实际: '{case['Actual']}'")
                    if len(failed_cases) > 3:
                        print(f"  ... 还有 {len(failed_cases) - 3} 个失败用例")
            else:
                print(f"\n--- 测试方法 {method} 失败 ---")
                print(f"错误信息: {result['message']}")
        
        # 输出该函数的汇总信息
        function_pass_rate = round((function_passed / function_cases) * 100, 2) if function_cases > 0 else 0
        print(f"\n{function_name} 函数汇总:")
        print(f"  支持的测试方法数: {function_methods}")
        print(f"  总测试用例数: {function_cases}")
        print(f"  通过用例数: {function_passed}")
        print(f"  失败用例数: {function_failed}")
        print(f"  整体通过率: {function_pass_rate}%")
    
    # 输出全局汇总信息
    overall_pass_rate = round((total_passed / total_cases) * 100, 2) if total_cases > 0 else 0
    
    print(f"\n{'='*80}")
    print("全局测试汇总报告")
    print("=" * 80)
    print(f"测试的函数数量: {total_functions}")
    print(f"执行的测试方法数: {total_methods}")
    print(f"总测试用例数: {total_cases}")
    print(f"通过用例数: {total_passed}")
    print(f"失败用例数: {total_failed}")
    print(f"整体通过率: {overall_pass_rate}%")
    
    # 按函数显示支持的测试方法
    print(f"\n{'='*60}")
    print("各函数支持的测试方法:")
    print("=" * 60)
    for function_name in SUPPORTED_FUNCTIONS:
        if function_name in TEST_CASES:
            methods = list(TEST_CASES[function_name]["test_methods"].keys())
            print(f"{function_name}:")
            for i, method in enumerate(methods, 1):
                method_name = TEST_CASES[function_name]["test_methods"][method]["name"]
                print(f"  {i}. {method} - {method_name}")
            print()
    
    print(f"{'='*80}")
    print("测试完成!")
    print("=" * 80)