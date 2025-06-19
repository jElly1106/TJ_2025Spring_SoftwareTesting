from flask import Blueprint, request, jsonify
from app.service.system_test.e2e_test import E2ETestService

system_test_bp = Blueprint('system_test', __name__)

@system_test_bp.route('/system/test/e2e/plot_detection', methods=['POST'])
def test_e2e_plot_detection():
    """
    端到端测试 - 地块检测功能
    
    请求体格式：
    {
        "test_config": {
            "base_url": "http://localhost:5174",
            "test_username": "testuser",
            "test_password": "testpass",
            "headless": false,
            "timeout": 30
        },
        "test_data": {
            "image_path": "test_images/disease_sample.jpg"
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "缺少请求参数"
            }), 400
        
        e2e_service = E2ETestService()
        result = e2e_service.run_plot_detection_test(
            test_config=data.get('test_config', {}),
            test_data=data.get('test_data', {})
        )
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
        }), 500

@system_test_bp.route('/system/test/e2e/plot_predefined_cases', methods=['GET'])
def get_e2e_predefined_cases():
    """
    获取端到端测试的预定义测试用例
    """
    try:
        e2e_service = E2ETestService()
        cases = e2e_service.get_predefined_test_cases()
        
        return jsonify({
            "success": True,
            "data": cases
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}"
        }), 500


@system_test_bp.route('/system/test/e2e/weather_info', methods=['POST'])
def test_e2e_weather_info():
    """
    端到端测试 - 用户查看天气信息功能
    
    请求体格式：
    {
        "test_config": {
            "base_url": "http://localhost:8100",
            "test_username": "testuser",
            "test_password": "testpass",
            "headless": false,
            "timeout": 30
        }
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "缺少请求参数"
            }), 400
        
        e2e_service = E2ETestService()
        result = e2e_service.run_weather_info_test(
            test_config=data.get('test_config', {})
        )
        
        return jsonify({
            "success": True,
            "data": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
        }), 500

@system_test_bp.route('/system/test/e2e/weather_predefined_cases', methods=['GET'])
def get_weather_e2e_predefined_cases():
    """
    获取天气信息测试的预定义测试用例
    """
    try:
        e2e_service = E2ETestService()
        cases = e2e_service.get_weather_predefined_test_cases()
        
        return jsonify({
            "success": True,
            "data": cases
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}"
        }), 500