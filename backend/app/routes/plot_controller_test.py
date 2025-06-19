from flask import Blueprint, request, jsonify
import asyncio
from app.service.plot_controller_test import PlotControllerTestService

# 创建蓝图
plot_controller_test_bp = Blueprint('plot_controller_test', __name__)

@plot_controller_test_bp.route('/plot/test/call_get_logs', methods=['POST'])
def test_call_get_logs():
    """
    测试call_get_logs函数
    """
    try:
        data = request.get_json()
        test_cases = data.get('test_cases', [])
        
        service = PlotControllerTestService()
        
        # 运行测试
        results = asyncio.run(service.run_call_get_logs_tests(test_cases))
        
        return jsonify({
            "status": "success",
            "message": "call_get_logs测试执行完成",
            "results": results
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"测试执行失败: {str(e)}"
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
    运行所有call_get_logs预定义测试用例
    """
    try:
        service = PlotControllerTestService()
        
        # 运行所有测试
        results = asyncio.run(service.run_call_get_logs_tests_batch())
        
        # 生成测试报告
        report = service.generate_test_report(results)
        
        return jsonify({
            "status": "success",
            "message": "所有call_get_logs测试执行完成",
            "results": results,
            "report": report
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"测试执行失败: {str(e)}"
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
        test_cases = data.get('test_cases', [])
        
        if not test_cases:
            return jsonify({
                "error": "请提供测试用例",
                "example": {
                    "test_cases": [
                        {
                            "case_id": "TC00901",
                            "description": "正常获取地块信息",
                            "test_type": "有效等价类",
                            "plotId": "plot123",
                            "expected_status": "success",
                            "expected_message": "返回完整Plot对象"
                        }
                    ]
                }
            }), 400
        
        service = PlotControllerTestService()
        results = asyncio.run(service.run_get_plot_by_id_tests(test_cases))
        
        return jsonify({
            "message": "get_plot_by_id测试完成",
            "results": results
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
        report = asyncio.run(service.run_get_plot_by_id_tests_batch())
        
        return jsonify({
            "message": "get_plot_by_id所有测试完成",
            "report": report
        })
        
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