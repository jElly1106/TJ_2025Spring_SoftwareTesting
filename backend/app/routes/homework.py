from flask import Blueprint, request, jsonify
import os
from app.static.homework_data import HOMEWORK_CODES, SUPPORTED_FUNCTIONS, SUPPORTED_TEST_METHODS
from app.service.homework import generate_test_cases
homework_bp = Blueprint('homework', __name__)

@homework_bp.route('/homework/code', methods=['GET'])
def get_homework_code():
    """
    获取题目的初始代码
    查询参数：
    - problem: 题目名称 (triangle_judge, computer_selling, telecom_system, calendar_problem)
    
    返回格式：
    {
        "success": true/false,
        "code": "代码字符串",
        "message": "提示信息"
    }
    """
    try:
        problem = request.args.get('problem')
        
        if not problem:
            return jsonify({
                "success": False,
                "code": "",
                "message": "缺少problem参数"
            }), 400
        
        if problem not in HOMEWORK_CODES:
            available_problems = list(HOMEWORK_CODES.keys())
            return jsonify({
                "success": False,
                "code": "",
                "message": f"题目不存在。可用题目：{', '.join(available_problems)}"
            }), 404
        
        return jsonify({
            "success": True,
            "code": HOMEWORK_CODES[problem],
            "message": "获取代码成功"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "code": "",
            "message": f"服务器错误：{str(e)}"
        }), 500
    
@homework_bp.route('/homework/test', methods=['POST'])
def run_test_cases():
    """
    运行测试用例生成和执行
    
    请求体格式（JSON）：
    {
        "code": "要测试的代码字符串",
        "function_name": "函数名称",
        "test_method": "测试方法名称"
    }
    
    返回格式：
    {
        "success": true/false,
        "message": "信息",
        "function_name": "函数名称",
        "test_method": "测试方法",
        "test_name": "测试名称",
        "description": "测试描述",
        "summary": {
            "total_cases": 总用例数,
            "passed_cases": 通过用例数,
            "failed_cases": 失败用例数,
            "pass_rate": "通过率百分比"
        },
        "test_results": [
            {
                "ID": 用例ID,
                "Input": 输入参数,
                "Expected": 期望结果,
                "Actual": 实际结果,
                "Passed": true/false,
                "Duration": "执行时间"
            }
        ]
    }
    """
    try:
        # 获取请求数据
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "请求体不能为空，需要JSON格式数据"
            }), 400
        
        # 验证必需参数
        code = data.get('code')
        function_name = data.get('function_name')
        test_method = data.get('test_method')
        
        if not code:
            return jsonify({
                "success": False,
                "message": "缺少必需参数：code"
            }), 400
        
        if not function_name:
            return jsonify({
                "success": False,
                "message": "缺少必需参数：function_name",
                "available_functions": SUPPORTED_FUNCTIONS
            }), 400
        
        if not test_method:
            return jsonify({
                "success": False,
                "message": "缺少必需参数：test_method",
                "available_methods": SUPPORTED_TEST_METHODS
            }), 400
        
        # 验证参数有效性
        if function_name not in SUPPORTED_FUNCTIONS:
            return jsonify({
                "success": False,
                "message": f"不支持的函数名称：{function_name}",
                "available_functions": SUPPORTED_FUNCTIONS
            }), 400
        
        if test_method not in SUPPORTED_TEST_METHODS:
            return jsonify({
                "success": False,
                "message": f"不支持的测试方法：{test_method}",
                "available_methods": SUPPORTED_TEST_METHODS
            }), 400
        
        # 调用测试用例生成函数
        result = generate_test_cases(code, function_name, test_method)
        
        # 根据结果返回相应的HTTP状态码
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"服务器内部错误：{str(e)}"
        }), 500
