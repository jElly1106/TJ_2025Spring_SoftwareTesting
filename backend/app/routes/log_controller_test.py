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
        
        # 统一数据格式
        total_tests = len(results)
        passed_tests = len([r for r in results if r["passed"]])
        failed_tests = total_tests - passed_tests
        
        # 按测试类型分组统计
        type_stats = {}
        for result in results:
            test_type = result["test_type"]
            if test_type not in type_stats:
                type_stats[test_type] = {"total": 0, "passed": 0, "failed": 0}
            type_stats[test_type]["total"] += 1
            if result["passed"]:
                type_stats[test_type]["passed"] += 1
            else:
                type_stats[test_type]["failed"] += 1
        
        # 计算平均执行时间
        avg_execution_time = sum(r["duration_ms"] for r in results) / total_tests if total_tests > 0 else 0
        
        return jsonify({
            "status": "success",
            "summary": {
                "total_cases": total_tests,
                "passed_cases": passed_tests,
                "failed_cases": failed_tests,
                "pass_rate": round((passed_tests / total_tests) * 100, 2) if total_tests > 0 else 0,
                "average_execution_time_ms": round(avg_execution_time, 2)
            },
            "statistics_by_type": type_stats,
            "test_results": results,
            "failed_cases": [r for r in results if not r["passed"]]
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
        
        # 统一数据格式
        total_tests = len(results)
        passed_tests = len([r for r in results if r["passed"]])
        failed_tests = total_tests - passed_tests
        
        # 按测试类型分组统计
        type_statistics = {}
        for result in results:
            test_type = result["test_type"]
            if test_type not in type_statistics:
                type_statistics[test_type] = {"total": 0, "passed": 0}
            type_statistics[test_type]["total"] += 1
            if result["passed"]:
                type_statistics[test_type]["passed"] += 1
        
        # 计算平均执行时间
        avg_execution_time = sum(r["duration_ms"] for r in results) / total_tests if total_tests > 0 else 0
        
        # 计算通过率
        pass_rate = f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0.0%"
        
        return jsonify({
            "success": True,
            "summary": {
                "total_cases": total_tests,
                "passed_cases": passed_tests,
                "failed_cases": failed_tests,
                "pass_rate": pass_rate,
                "avg_duration_ms": round(avg_execution_time, 2),
                "type_statistics": type_statistics
            },
            "test_results": results
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@log_test_bp.route('/set_log_function_source', methods=['GET'])
def get_set_log_function_source():
    """
    获取 set_log 函数的源代码
    """
    try:
        source_info = log_test_service.get_set_log_function_source_code()
        return jsonify({
            "status": "success",
            "message": "获取函数源代码成功",
            "source_info": source_info
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"获取源代码失败: {str(e)}"
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