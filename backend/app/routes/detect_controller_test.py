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
    测试validate_plot_access函数（直接调用）
    
    请求体格式：
    {
        "test_cases": [
            {
                "test_id": "IT_TC_007_001",
                "test_purpose": "有效地块ID，授权用户访问",
                "case_id": "001",
                "plotId": "valid_plot_id_123",
                "userId": "user_123",
                "expected_status": 200,
                "expected_message": "验证成功",
                "test_type": "有效等价类"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        if not data or 'test_cases' not in data:
            return jsonify({
                "success": False,
                "message": "缺少test_cases参数"
            }), 400
        
        test_service = DetectTestService()
        
        # 使用 asyncio 运行异步测试
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(
                test_service.run_validate_plot_access_tests(data['test_cases'])
            )
            report = test_service.generate_test_report(results)
        finally:
            loop.close()
        
        return jsonify({
            "success": True,
            "message": "测试执行完成",
            "report": report,
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
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
    运行所有预定义的validate_plot_access测试用例
    """
    try:
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
        
        return jsonify({
            "success": True,
            "message": "批量测试执行完成",
            "report": report,
            "results": results
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"批量测试执行失败: {str(e)}"
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