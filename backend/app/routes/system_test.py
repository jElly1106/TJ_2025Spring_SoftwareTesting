from flask import Blueprint, request, jsonify
import traceback
import os

# 更新导入语句
from app.service.system_test.e2e_test import E2ETestService
from app.service.system_test.utils import E2ETestUtils
from app.service.system_test.config import E2ETestConfig

system_test_bp = Blueprint('system_test', __name__)

@system_test_bp.route('/system/test/e2e/plot_detection', methods=['POST'])
def test_e2e_plot_detection():
    """端到端测试 - 地块检测功能"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "缺少请求参数",
                "error_code": "MISSING_PARAMS"
            }), 400
        
        # 验证和标准化配置
        try:
            test_config = E2ETestUtils.validate_test_config(data.get('test_config', {}))
            test_data = E2ETestUtils.validate_test_data(data.get('test_data', {}))
        except ValueError as e:
            return jsonify({
                "success": False,
                "message": f"配置验证失败: {str(e)}",
                "error_code": "CONFIG_VALIDATION_ERROR"
            }), 400
        
        # 执行测试
        e2e_service = E2ETestService()
        result = e2e_service.run_plot_detection_test(
            test_config=test_config,
            test_data=test_data
        )
        
        # 根据测试结果返回相应的HTTP状态码
        if result.get("status") == "PASSED":
            return jsonify({
                "success": True,
                "data": result,
                "message": "地块检测测试执行成功"
            })
        else:
            return jsonify({
                "success": False,
                "data": result,
                "message": f"地块检测测试执行失败: {result.get('message', '未知错误')}"
            }), 422
        
    except Exception as e:
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        
        print(f"系统测试执行出错: {error_details}")
        
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}",
            "error_code": "SYSTEM_ERROR",
            "error_details": error_details if request.args.get('debug') == 'true' else None
        }), 500

@system_test_bp.route('/system/test/e2e/plot_detection_predefined_cases', methods=['GET'])
def get_plot_detection_predefined_cases():
    """获取地块检测测试的预定义测试用例"""
    try:
        e2e_service = E2ETestService()
        cases = e2e_service.get_predefined_test_cases()
        
        return jsonify({
            "success": True,
            "data": cases,
            "count": len(cases),
            "message": "获取预定义用例成功"
        })
        
    except Exception as e:
        print(f"获取预定义用例失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}",
            "error_code": "GET_CASES_ERROR"
        }), 500

@system_test_bp.route('/system/test/e2e/weather_info', methods=['POST'])
def test_e2e_weather_info():
    """端到端测试 - 用户查看天气信息功能"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "缺少请求参数",
                "error_code": "MISSING_PARAMS"
            }), 400
        
        # 验证配置
        try:
            test_config = E2ETestUtils.validate_test_config(data.get('test_config', {}))
        except ValueError as e:
            return jsonify({
                "success": False,
                "message": f"配置验证失败: {str(e)}",
                "error_code": "CONFIG_VALIDATION_ERROR"
            }), 400
        
        # 执行测试
        e2e_service = E2ETestService()
        result = e2e_service.run_weather_info_test(test_config=test_config)
        
        # 根据测试结果返回相应状态码
        if result.get("status") == "PASSED":
            return jsonify({
                "success": True,
                "data": result,
                "message": "天气信息测试执行成功"
            })
        else:
            return jsonify({
                "success": False,
                "data": result,
                "message": f"天气信息测试执行失败: {result.get('message', '未知错误')}"
            }), 422
        
    except Exception as e:
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        
        print(f"天气信息测试执行出错: {error_details}")
        
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}",
            "error_code": "SYSTEM_ERROR",
            "error_details": error_details if request.args.get('debug') == 'true' else None
        }), 500

@system_test_bp.route('/system/test/e2e/weather_info_predefined_cases', methods=['GET'])
def get_weather_info_predefined_cases():
    """获取天气信息测试的预定义测试用例"""
    try:
        e2e_service = E2ETestService()
        cases = e2e_service.get_weather_predefined_test_cases()
        
        return jsonify({
            "success": True,
            "data": cases,
            "count": len(cases),
            "message": "获取天气测试预定义用例成功"
        })
        
    except Exception as e:
        print(f"获取天气测试预定义用例失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}",
            "error_code": "GET_WEATHER_CASES_ERROR"
        }), 500

@system_test_bp.route('/system/test/e2e/plot_management', methods=['POST'])
def test_e2e_plot_management():
    """端到端测试 - 地块管理功能（创建+删除）"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "缺少请求参数",
                "error_code": "MISSING_PARAMS"
            }), 400
        
        # 验证配置
        try:
            test_config = E2ETestUtils.validate_test_config(data.get('test_config', {}))
        except ValueError as e:
            return jsonify({
                "success": False,
                "message": f"配置验证失败: {str(e)}",
                "error_code": "CONFIG_VALIDATION_ERROR"
            }), 400
        
        # 执行测试
        e2e_service = E2ETestService()
        result = e2e_service.run_plot_management_test(test_config=test_config)
        
        # 根据测试结果返回相应状态码
        if result.get("status") == "PASSED":
            return jsonify({
                "success": True,
                "data": result,
                "message": "地块管理测试执行成功"
            })
        else:
            return jsonify({
                "success": False,
                "data": result,
                "message": f"地块管理测试执行失败: {result.get('message', '未知错误')}"
            }), 422
        
    except Exception as e:
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        
        print(f"地块管理测试执行出错: {error_details}")
        
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}",
            "error_code": "SYSTEM_ERROR",
            "error_details": error_details if request.args.get('debug') == 'true' else None
        }), 500

@system_test_bp.route('/system/test/e2e/plot_management_predefined_cases', methods=['GET'])
def get_plot_management_predefined_cases():
    """获取地块管理测试的预定义测试用例"""
    try:
        e2e_service = E2ETestService()
        cases = e2e_service.get_plot_management_predefined_test_cases()
        
        return jsonify({
            "success": True,
            "data": cases,
            "count": len(cases),
            "message": "获取地块管理测试预定义用例成功"
        })
        
    except Exception as e:
        print(f"获取地块管理测试预定义用例失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}",
            "error_code": "GET_PLOT_MANAGEMENT_CASES_ERROR"
        }), 500

@system_test_bp.route('/system/test/e2e/plot_logs', methods=['POST'])
def test_e2e_plot_logs():
    """端到端测试 - 地块日志查看功能"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "缺少请求参数",
                "error_code": "MISSING_PARAMS"
            }), 400
        
        # 验证配置
        try:
            test_config = E2ETestUtils.validate_test_config(data.get('test_config', {}))
        except ValueError as e:
            return jsonify({
                "success": False,
                "message": f"配置验证失败: {str(e)}",
                "error_code": "CONFIG_VALIDATION_ERROR"
            }), 400
        
        # 执行测试
        e2e_service = E2ETestService()
        result = e2e_service.run_plot_logs_test(test_config=test_config)
        
        # 根据测试结果返回相应状态码
        if result.get("status") == "PASSED":
            return jsonify({
                "success": True,
                "data": result,
                "message": "地块日志查看测试执行成功"
            })
        else:
            return jsonify({
                "success": False,
                "data": result,
                "message": f"地块日志查看测试执行失败: {result.get('message', '未知错误')}"
            }), 422
        
    except Exception as e:
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        
        print(f"地块日志测试执行出错: {error_details}")
        
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}",
            "error_code": "SYSTEM_ERROR",
            "error_details": error_details if request.args.get('debug') == 'true' else None
        }), 500

@system_test_bp.route('/system/test/e2e/plot_logs_predefined_cases', methods=['GET'])
def get_plot_logs_predefined_cases():
    """获取地块日志测试的预定义测试用例"""
    try:
        e2e_service = E2ETestService()
        cases = e2e_service.get_plot_logs_predefined_test_cases()
        
        return jsonify({
            "success": True,
            "data": cases,
            "count": len(cases),
            "message": "获取地块日志测试预定义用例成功"
        })
        
    except Exception as e:
        print(f"获取地块日志测试预定义用例失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}",
            "error_code": "GET_PLOT_LOGS_CASES_ERROR"
        }), 500

# ⚠️ 批量测试路由 - 只保留一个定义
@system_test_bp.route('/system/test/e2e/batch', methods=['POST'])
def run_batch_e2e_tests():
    """
    批量执行端到端测试
    
    支持的测试类型：
    - plot_detection: 地块检测测试
    - weather_info: 天气信息测试
    - plot_management: 地块管理测试
    - plot_logs: 地块日志查看测试（新增）
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "缺少请求参数",
                "error_code": "MISSING_PARAMS"
            }), 400
        
        # 验证配置和数据
        try:
            test_config = E2ETestUtils.validate_test_config(data.get('test_config', {}))
            test_data = E2ETestUtils.validate_test_data(data.get('test_data', {}))
        except ValueError as e:
            return jsonify({
                "success": False,
                "message": f"配置验证失败: {str(e)}",
                "error_code": "CONFIG_VALIDATION_ERROR"
            }), 400
        
        test_types = data.get('test_types', ['plot_detection', 'weather_info', 'plot_management', 'plot_logs'])
        
        results = []
        e2e_service = E2ETestService()
        
        for test_type in test_types:
            try:
                print(f"\n[批量测试] 开始执行测试类型: {test_type}")
                
                if test_type == 'plot_detection':
                    result = e2e_service.run_plot_detection_test(test_config, test_data)
                elif test_type == 'weather_info':
                    result = e2e_service.run_weather_info_test(test_config)
                elif test_type == 'plot_management':
                    result = e2e_service.run_plot_management_test(test_config)
                elif test_type == 'plot_logs':
                    result = e2e_service.run_plot_logs_test(test_config)
                else:
                    result = {
                        "test_type": test_type,
                        "status": "SKIPPED",
                        "message": f"未知的测试类型: {test_type}",
                        "start_time": None,
                        "end_time": None,
                        "execution_time": 0
                    }
                
                result["test_type"] = test_type
                results.append(result)
                
                print(f"[批量测试] 测试类型 {test_type} 完成，状态: {result.get('status')}")
                
            except Exception as e:
                error_result = {
                    "test_type": test_type,
                    "status": "FAILED",
                    "error_message": str(e),
                    "message": f"测试类型 {test_type} 执行失败",
                    "start_time": None,
                    "end_time": None,
                    "execution_time": 0
                }
                results.append(error_result)
                print(f"[批量测试] 测试类型 {test_type} 执行失败: {str(e)}")
        
        # 生成综合报告
        report = E2ETestUtils.generate_test_report(results)
        
        return jsonify({
            "success": True,
            "data": report,
            "message": f"批量测试完成，通过率: {report['summary']['pass_rate']}%"
        })
        
    except Exception as e:
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        
        print(f"批量测试执行出错: {error_details}")
        
        return jsonify({
            "success": False,
            "message": f"批量测试执行失败: {str(e)}",
            "error_code": "BATCH_TEST_ERROR",
            "error_details": error_details if request.args.get('debug') == 'true' else None
        }), 500

@system_test_bp.route('/system/test/environment/validate', methods=['GET'])
def validate_test_environment():
    """验证测试环境"""
    try:
        validation_result = E2ETestUtils.validate_browser_environment()
        
        if validation_result["environment_ready"]:
            return jsonify({
                "success": True,
                "data": validation_result,
                "message": "测试环境验证通过"
            })
        else:
            return jsonify({
                "success": False,
                "data": validation_result,
                "message": "测试环境验证失败",
                "error_code": "ENVIRONMENT_NOT_READY"
            }), 422
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"环境验证失败: {str(e)}",
            "error_code": "ENVIRONMENT_VALIDATION_ERROR"
        }), 500

@system_test_bp.route('/system/test/cleanup', methods=['POST'])
def cleanup_test_files():
    """清理测试文件"""
    try:
        data = request.get_json() or {}
        keep_recent = data.get('keep_recent', 5)
        
        E2ETestUtils.cleanup_test_files(keep_recent=keep_recent)
        
        return jsonify({
            "success": True,
            "message": f"测试文件清理完成，保留最近 {keep_recent} 个文件"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"清理测试文件失败: {str(e)}",
            "error_code": "CLEANUP_ERROR"
        }), 500

# === 删除所有重复的路由定义 ===
# 确保文件中没有重复的以下路由：
# - @system_test_bp.route('/system/test/e2e/batch', methods=['POST'])
# - 任何其他重复的路由定义

# === 错误处理中间件 ===
@system_test_bp.errorhandler(400)
def handle_bad_request(error):
    """处理400错误"""
    return jsonify({
        "success": False,
        "message": "请求格式错误",
        "error_code": "BAD_REQUEST"
    }), 400

@system_test_bp.errorhandler(404)
def handle_not_found(error):
    """处理404错误"""
    return jsonify({
        "success": False,
        "message": "请求的资源不存在",
        "error_code": "NOT_FOUND"
    }), 404

@system_test_bp.errorhandler(500)
def handle_internal_error(error):
    """处理500错误"""
    return jsonify({
        "success": False,
        "message": "内部服务器错误",
        "error_code": "INTERNAL_ERROR"
    }), 500