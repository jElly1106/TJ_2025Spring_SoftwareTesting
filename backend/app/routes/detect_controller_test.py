from flask import Blueprint, request, jsonify
from typing import List, Dict, Any
from app.service.detect_controller_test import DetectTestService
import asyncio

detect_test_bp = Blueprint('detect_test', __name__)

@detect_test_bp.route('/detect/test/function_source', methods=['GET'])
def get_function_source():
    """
    获取 validate_plot_access 函数的源代码
    """
    try:
        test_service = DetectTestService()
        source_info = test_service.get_function_source_code()
        
        return jsonify({
            "success": True,
            "message": "获取函数源代码成功",
            "source_info": source_info
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取函数源代码失败: {str(e)}"
        }), 500

@detect_test_bp.route('/detect/test/validate_plot_access', methods=['POST'])
def test_validate_plot_access():
    """
    执行单个validate_plot_access测试用例
    """
    try:
        data = request.get_json()
        test_case = data.get('test_case')
        
        if not test_case:
            return jsonify({
                "success": False,
                "error": "Missing test_case in request"
            }), 400
        
        # 创建服务实例
        service = DetectTestService()
        
        # 执行单个测试
        result = asyncio.run(service._execute_validate_plot_access_test(test_case))
        
        # 返回统一格式
        return jsonify({
            "success": True,
            "summary": {
                "total_cases": 1,
                "passed_cases": 1 if result['passed'] else 0,
                "failed_cases": 0 if result['passed'] else 1,
                "pass_rate": "100.0%" if result['passed'] else "0.0%",
                "avg_duration_ms": result['duration_ms'],
                "type_statistics": {
                    result['test_type']: {
                        "total": 1,
                        "passed": 1 if result['passed'] else 0
                    }
                }
            },
            "test_results": [result]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@detect_test_bp.route('/detect/test/validate_plot_access_predefined_cases', methods=['GET'])
def get_validate_plot_access_predefined_cases():
    """
    获取validate_plot_access函数的预定义测试用例
    """
    try:
        test_service = DetectTestService()
        cases = test_service.get_validate_plot_access_predefined_cases()
        
        return jsonify({
            "success": True,
            "message": "获取预定义测试用例成功",
            "total_cases": len(cases),
            "test_cases": cases
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取预定义测试用例失败: {str(e)}"
        }), 500

@detect_test_bp.route('/detect/test/run_validate_plot_access_all_tests', methods=['POST'])
def run_validate_plot_access_all_tests():
    """
    运行所有validate_plot_access测试用例
    """
    try:
        service = DetectTestService()
        result = asyncio.run(service.run_validate_plot_access_tests_batch())
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        
@detect_test_bp.route('/detect/test/validate_plot_access_report', methods=['POST'])
def get_validate_plot_access_report():
    """
    获取详细的测试报告（包含函数源代码）
    
    请求体格式：
    {
        "include_details": true,
        "include_source_code": true
    }
    """
    try:
        data = request.get_json() or {}
        include_details = data.get('include_details', False)
        include_source_code = data.get('include_source_code', True)
        
        test_service = DetectTestService()
        
        # 使用 asyncio 运行异步测试
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(
                test_service.run_validate_plot_access_tests_batch()
            )
            report = test_service.generate_test_report(results)
        finally:
            loop.close()
        
        response_data = {
            "success": True,
            "message": "测试报告生成完成",
            "report": report
        }
        
        if include_details:
            response_data["detailed_results"] = results
        
        if include_source_code:
            response_data["function_source"] = test_service.get_function_source_code()
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"生成测试报告失败: {str(e)}"
        }), 500