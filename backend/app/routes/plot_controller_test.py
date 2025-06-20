from flask import Blueprint, request, jsonify
import asyncio
import time
from app.service.plot_controller_test import PlotControllerTestService


# 创建蓝图
plot_controller_test_bp = Blueprint('plot_controller_test', __name__)

@plot_controller_test_bp.route('/plot/test/call_get_logs', methods=['POST'])
def test_call_get_logs():
    """
    执行单个call_get_logs测试用例
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
        service = PlotControllerTestService()
        
        # 执行单个测试
        result = asyncio.run(service._execute_call_get_logs_test(test_case))
        
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

@plot_controller_test_bp.route('/plot/test/call_get_logs_predefined_cases', methods=['GET'])
def get_call_get_logs_predefined_cases():
    """
    获取call_get_logs的预定义测试用例
    """
    try:
        service = PlotControllerTestService()
        test_cases = service.get_call_get_logs_predefined_cases()
        
        return jsonify({
            "status": "success",
            "message": "获取预定义测试用例成功",
            "test_cases": test_cases,
            "total_count": len(test_cases)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"获取测试用例失败: {str(e)}"
        }), 500

@plot_controller_test_bp.route('/plot/test/run_call_get_logs_all_tests', methods=['POST'])
def run_call_get_logs_all_tests():
    """
    运行所有call_get_logs测试用例
    """
    try:
        service = PlotControllerTestService()
        result = asyncio.run(service.run_call_get_logs_tests_batch())
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@plot_controller_test_bp.route('/plot/test/call_get_logs_function_source', methods=['GET'])
def get_call_get_logs_function_source():
    """
    获取call_get_logs函数的源代码
    """
    try:
        service = PlotControllerTestService()
        source_info = service.get_call_get_logs_function_source_code()
        
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

@plot_controller_test_bp.route('/plot/test/call_get_logs_report', methods=['POST'])
def generate_call_get_logs_report():
    """
    生成call_get_logs测试报告
    """
    try:
        data = request.get_json()
        results = data.get('results', [])
        
        service = PlotControllerTestService()
        report = service.generate_test_report(results)
        
        return jsonify({
            "status": "success",
            "message": "测试报告生成成功",
            "report": report
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"报告生成失败: {str(e)}"
        }), 500


@plot_controller_test_bp.route('/plot/test/get_plot_by_id', methods=['POST'])
def test_get_plot_by_id():
    """
    测试get_plot_by_id函数
    """
    try:
        data = request.get_json()
        test_case = data
        
        service = PlotControllerTestService()
        result = asyncio.run(service._execute_get_plot_by_id_test(test_case))
        
        # 计算统计信息
        total_cases = 1
        passed_cases = 1 if result['passed'] else 0
        failed_cases = total_cases - passed_cases
        pass_rate = f"{(passed_cases/total_cases*100):.1f}%"
        avg_duration_ms = result.get('duration_ms', 0)
        
        # 按测试类型统计
        test_type = result['test_type']
        type_statistics = {
            test_type: {
                "total": 1,
                "passed": passed_cases,
                "pass_rate": pass_rate
            }
        }
        
        return jsonify({
            "success": True,
            "summary": {
                "total_cases": total_cases,
                "passed_cases": passed_cases,
                "failed_cases": failed_cases,
                "pass_rate": pass_rate,
                "avg_duration_ms": avg_duration_ms,
                "type_statistics": type_statistics
            },
            "test_result": result
        })
        
    except Exception as e:
        return jsonify({"error": f"测试执行失败: {str(e)}"}), 500

@plot_controller_test_bp.route('/plot/test/get_plot_by_id_predefined_cases', methods=['GET'])
def get_get_plot_by_id_predefined_cases():
    """
    获取get_plot_by_id函数的预定义测试用例
    """
    try:
        service = PlotControllerTestService()
        test_cases = service.get_get_plot_by_id_predefined_cases()
        
        return jsonify({
            "message": "获取预定义测试用例成功",
            "test_cases": test_cases,
            "total_cases": len(test_cases)
        })
        
    except Exception as e:
        return jsonify({"error": f"获取测试用例失败: {str(e)}"}), 500

@plot_controller_test_bp.route('/plot/test/run_get_plot_by_id_all_tests', methods=['POST'])
def run_get_plot_by_id_all_tests():
    """
    运行所有get_plot_by_id预定义测试用例并生成报告
    """
    try:
        service = PlotControllerTestService()
        result = asyncio.run(service.run_get_plot_by_id_tests_batch())
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"批量测试执行失败: {str(e)}"}), 500
        
@plot_controller_test_bp.route('/plot/test/get_plot_by_id_function_source', methods=['GET'])
def get_get_plot_by_id_function_source():
    """
    获取get_plot_by_id函数的源代码
    """
    try:
        service = PlotControllerTestService()
        source_code = service.get_get_plot_by_id_function_source_code()
        
        return jsonify({
            "message": "获取函数源代码成功",
            "function_name": "get_plot_by_id",
            "source_code": source_code
        })
        
    except Exception as e:
        return jsonify({"error": f"获取源代码失败: {str(e)}"}), 500

@plot_controller_test_bp.route('/plot/test/get_plot_by_id_report', methods=['POST'])
def generate_get_plot_by_id_report():
    """
    生成get_plot_by_id测试报告
    """
    try:
        data = request.get_json()
        test_results = data.get('test_results', [])
        
        if not test_results:
            return jsonify({"error": "请提供测试结果数据"}), 400
        
        service = PlotControllerTestService()
        report = asyncio.run(service.generate_get_plot_by_id_test_report(test_results))
        
        return jsonify({
            "message": "测试报告生成成功",
            "report": report
        })
        
    except Exception as e:
        return jsonify({"error": f"报告生成失败: {str(e)}"}), 500