from flask import Blueprint, request, jsonify
from typing import List, Dict, Any
from app.service.plot_test import PlotTestService

plot_test_bp = Blueprint('plot_test', __name__)

'''
    测试add_plot接口
'''

@plot_test_bp.route('/plot/test/add_plot', methods=['POST'])
def test_add_plot():
    """
    测试add_plot接口
    
    请求体格式：
    {
        "test_cases": [
            {
                "test_id": "IT_TC_005_001",
                "test_purpose": "正常添加地块",
                "case_id": "001",
                "plotName": "地块A",
                "plantName": "水稻",
                "expected_status": 200,
                "expected_message": "地块创建成功",
                "test_type": "有效等价类"
            }
        ],
        "auth_token": "your_auth_token_here"
    }
    """
    try:
        data = request.get_json()
        if not data or 'test_cases' not in data:
            return jsonify({
                "success": False,
                "message": "缺少test_cases参数"
            }), 400
        
        test_service = PlotTestService()
        
        # 设置认证token（如果提供）
        if 'auth_token' in data:
            test_service.set_auth_token(data['auth_token'])
        
        results = test_service.run_plot_input_tests(data['test_cases'])
        
        return jsonify({
            "success": True,
            "test_results": results,
            "summary": test_service.generate_module_summary(results, "add_plot")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
        }), 500

@plot_test_bp.route('/plot/test/predefined_cases', methods=['GET'])
def get_plot_predefined_cases():
    """
    获取add_plot接口的预定义测试用例
    """
    try:
        test_service = PlotTestService()
        cases = test_service.get_plot_predefined_cases()
        
        return jsonify({
            "success": True,
            "test_cases": cases,
            "total_count": len(cases)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}"
        }), 500

@plot_test_bp.route('/plot/test/run_all_tests', methods=['POST'])
def run_all_plot_tests():
    """
    执行所有add_plot预定义测试用例
    
    请求体格式（可选）：
    {
        "stop_on_failure": false,
        "auth_token": "your_auth_token_here"
    }
    """
    try:
        data = request.get_json() or {}
        stop_on_failure = data.get('stop_on_failure', False)
        
        test_service = PlotTestService()
        
        # 设置认证token（如果提供）
        if 'auth_token' in data:
            test_service.set_auth_token(data['auth_token'])
        
        predefined_cases = test_service.get_plot_predefined_cases()
        
        batch_result = test_service.run_plot_tests_batch(
            predefined_cases, 
            stop_on_failure=stop_on_failure
        )
        
        return jsonify({
            "success": True,
            "test_results": batch_result["test_results"],  # 直接提取test_results
            "execution_info": batch_result["execution_info"],  # 添加执行信息
            "summary": test_service.generate_module_summary(
                batch_result["test_results"], 
                "add_plot"
            )
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"批量测试执行失败: {str(e)}"
        }), 500

'''
    测试get_plot_detail接口
'''

@plot_test_bp.route('/plot/test/get_plot_detail', methods=['POST'])
def test_get_plot_detail():
    """
    测试get_plot_detail接口
    
    请求体格式：
    {
        "test_cases": [
            {
                "test_id": "IT_TC_006_001",
                "test_purpose": "正常获取地块详情",
                "case_id": "001",
                "plotId": "存在的合法ID",
                "user_status": "已登录",
                "expected_status": 200,
                "expected_message": "返回PlotDetails",
                "test_type": "有效等价类"
            }
        ],
        "auth_token": "your_auth_token_here"
    }
    """
    try:
        data = request.get_json()
        if not data or 'test_cases' not in data:
            return jsonify({
                "success": False,
                "message": "缺少test_cases参数"
            }), 400
        
        test_service = PlotTestService()
        
        # 设置认证token（如果提供）
        if 'auth_token' in data:
            test_service.set_auth_token(data['auth_token'])
        
        results = test_service.run_plot_detail_input_tests(data['test_cases'])
        
        return jsonify({
            "success": True,
            "test_results": results,
            "summary": test_service.generate_module_summary(results, "get_plot_detail")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
        }), 500

@plot_test_bp.route('/plot/test/plot_detail_predefined_cases', methods=['GET'])
def get_plot_detail_predefined_cases():
    """
    获取get_plot_detail接口的预定义测试用例
    """
    try:
        test_service = PlotTestService()
        cases = test_service.get_plot_detail_predefined_cases()
        
        return jsonify({
            "success": True,
            "test_cases": cases,
            "total_count": len(cases)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}"
        }), 500

@plot_test_bp.route('/plot/test/run_plot_detail_all_tests', methods=['POST'])
def run_all_plot_detail_tests():
    """
    执行所有get_plot_detail预定义测试用例
    
    请求体格式（可选）：
    {
        "stop_on_failure": false,
        "auth_token": "your_auth_token_here"
    }
    """
    try:
        data = request.get_json() or {}
        stop_on_failure = data.get('stop_on_failure', False)
        
        test_service = PlotTestService()
        
        # 设置认证token（如果提供）
        if 'auth_token' in data:
            test_service.set_auth_token(data['auth_token'])
        
        batch_result = test_service.run_plot_detail_tests_batch(
            stop_on_failure=stop_on_failure
        )
        
        return jsonify({
            "success": True,
            "test_results": batch_result["test_results"],  # 只返回测试结果部分
            "execution_info": batch_result["execution_info"],  # 添加执行信息
            "summary": test_service.generate_module_summary(
                batch_result["test_results"], 
                "get_plot_detail"
            )
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"批量测试执行失败: {str(e)}"
        }), 500