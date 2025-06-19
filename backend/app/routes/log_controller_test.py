from flask import Blueprint, request, jsonify
import asyncio
from app.service.log_controller_test import LogControllerTestService

# 创建蓝图
log_test_bp = Blueprint('log_test', __name__, url_prefix='/log/test')

# 创建服务实例
log_test_service = LogControllerTestService()

@log_test_bp.route('/set_log', methods=['POST'])
def test_set_log():
    """
    运行指定的 set_log 测试用例
    """
    try:
        data = request.get_json()
        if not data or 'test_cases' not in data:
            return jsonify({
                "error": "Missing test_cases in request body",
                "message": "请在请求体中提供test_cases字段"
            }), 400
        
        test_cases = data['test_cases']
        results = asyncio.run(log_test_service.run_set_log_tests(test_cases))
        
        return jsonify({
            "status": "success",
            "results": results,
            "summary": {
                "total": len(results),
                "passed": len([r for r in results if r["status"] == "PASS"]),
                "failed": len([r for r in results if r["status"] == "FAIL"])
            }
        })
    
    except Exception as e:
        return jsonify({
            "error": "Test execution failed",
            "message": str(e)
        }), 500

@log_test_bp.route('/set_log_predefined_cases', methods=['GET'])
def get_set_log_predefined_cases():
    """
    获取 set_log 函数的预定义测试用例
    """
    try:
        cases = log_test_service.get_set_log_predefined_cases()
        return jsonify({
            "status": "success",
            "test_cases": cases,
            "total_count": len(cases)
        })
    except Exception as e:
        return jsonify({
            "error": "Failed to get predefined cases",
            "message": str(e)
        }), 500

@log_test_bp.route('/run_set_log_all_tests', methods=['POST'])
def run_set_log_all_tests():
    """
    运行所有预定义的 set_log 测试用例并生成报告
    """
    try:
        results = asyncio.run(log_test_service.run_set_log_tests_batch())
        report = log_test_service.generate_test_report(results)
        
        return jsonify({
            "status": "success",
            "report": report
        })
    
    except Exception as e:
        return jsonify({
            "error": "Batch test execution failed",
            "message": str(e)
        }), 500

@log_test_bp.route('/set_log_function_source', methods=['GET'])
def get_set_log_function_source():
    """
    获取 set_log 函数的源代码
    """
    try:
        source_code = log_test_service.get_set_log_function_source_code()
        return jsonify({
            "status": "success",
            "source_code": source_code,
            "function_name": "set_log"
        })
    except Exception as e:
        return jsonify({
            "error": "Failed to get function source",
            "message": str(e)
        }), 500

@log_test_bp.route('/set_log_report', methods=['POST'])
def generate_set_log_report():
    """
    根据提供的测试结果生成报告
    """
    try:
        data = request.get_json()
        if not data or 'test_results' not in data:
            return jsonify({
                "error": "Missing test_results in request body",
                "message": "请在请求体中提供test_results字段"
            }), 400
        
        test_results = data['test_results']
        report = log_test_service.generate_test_report(test_results)
        
        return jsonify({
            "status": "success",
            "report": report
        })
    
    except Exception as e:
        return jsonify({
            "error": "Report generation failed",
            "message": str(e)
        }), 500