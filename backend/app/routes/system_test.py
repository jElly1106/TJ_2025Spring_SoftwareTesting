from flask import Blueprint, request, jsonify
from app.service.system_test.e2e_test import E2ETestService, E2ETestUtils
import traceback
import os

system_test_bp = Blueprint('system_test', __name__)

@system_test_bp.route('/system/test/e2e/plot_detection', methods=['POST'])
def test_e2e_plot_detection():
    """
    端到端测试 - 地块检测功能
    
    请求体格式：
    {
        "test_config": {
            "base_url": "http://47.120.78.249:8000",
            "test_username": "testuser",
            "test_password": "testpass",
            "headless": false,
            "timeout": 30
        },
        "test_data": {
            "image_path": "test_data/disease_sample.jpg"
        }
    }
    """
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
            }), 422  # 测试失败但请求格式正确
        
    except Exception as e:
        # 记录详细错误信息
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
    """
    端到端测试 - 用户查看天气信息功能
    
    请求体格式：
    {
        "test_config": {
            "base_url": "http://47.120.78.249:8000",
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

# === 新增的API接口 ===

@system_test_bp.route('/system/test/e2e/batch', methods=['POST'])
def run_batch_e2e_tests():
    """
    批量执行端到端测试
    
    请求体格式：
    {
        "test_config": {
            "base_url": "http://47.120.78.249:8000",
            "test_username": "testuser",
            "test_password": "testpass",
            "headless": true,
            "timeout": 30
        },
        "test_types": ["plot_detection", "weather_info"],
        "test_data": {
            "image_path": "test_data/disease_sample.jpg"
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
        
        test_config = E2ETestUtils.validate_test_config(data.get('test_config', {}))
        test_types = data.get('test_types', ['plot_detection', 'weather_info'])
        test_data = E2ETestUtils.validate_test_data(data.get('test_data', {}))
        
        results = []
        e2e_service = E2ETestService()
        
        for test_type in test_types:
            try:
                if test_type == 'plot_detection':
                    result = e2e_service.run_plot_detection_test(test_config, test_data)
                elif test_type == 'weather_info':
                    result = e2e_service.run_weather_info_test(test_config)
                else:
                    result = {
                        "test_type": test_type,
                        "status": "SKIPPED",
                        "message": f"未知的测试类型: {test_type}"
                    }
                
                result["test_type"] = test_type
                results.append(result)
                
            except Exception as e:
                results.append({
                    "test_type": test_type,
                    "status": "FAILED",
                    "error_message": str(e),
                    "message": f"测试类型 {test_type} 执行失败"
                })
        
        # 生成综合报告
        report = E2ETestUtils.generate_test_report(results)
        
        return jsonify({
            "success": True,
            "data": report,
            "message": f"批量测试完成，通过率: {report['summary']['pass_rate']}%"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"批量测试执行失败: {str(e)}"
        }), 500

@system_test_bp.route('/system/test/e2e/config/validate', methods=['POST'])
def validate_test_config():
    """
    验证测试配置
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "message": "缺少配置数据"
            }), 400
        
        # 验证配置
        validated_config = E2ETestUtils.validate_test_config(data.get('test_config', {}))
        validated_data = E2ETestUtils.validate_test_data(data.get('test_data', {}))
        
        return jsonify({
            "success": True,
            "data": {
                "validated_config": validated_config,
                "validated_data": validated_data
            },
            "message": "配置验证成功"
        })
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "message": f"配置验证失败: {str(e)}",
            "error_code": "VALIDATION_ERROR"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"验证过程出错: {str(e)}"
        }), 500

@system_test_bp.route('/system/test/e2e/health', methods=['GET'])
def check_test_environment():
    """
    检查测试环境健康状态
    """
    try:
        health_status = {
            "chrome_available": False,
            "test_directories": {},
            "selenium_version": None,
            "issues": []
        }
        
        # 检查Chrome可用性
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=chrome_options)
            health_status["chrome_available"] = True
            health_status["chrome_version"] = driver.capabilities.get('browserVersion')
            driver.quit()
            
        except Exception as e:
            health_status["issues"].append(f"Chrome不可用: {str(e)}")
        
        # 检查测试目录
        e2e_service = E2ETestService()
        test_dirs = {
            "test_data": e2e_service.test_data_dir,
            "screenshots": e2e_service.screenshot_dir
        }
        
        for name, path in test_dirs.items():
            health_status["test_directories"][name] = {
                "path": path,
                "exists": os.path.exists(path),
                "writable": os.access(path, os.W_OK) if os.path.exists(path) else False
            }
            
            if not os.path.exists(path):
                health_status["issues"].append(f"测试目录不存在: {path}")
        
        # 检查Selenium版本
        try:
            import selenium
            health_status["selenium_version"] = selenium.__version__
        except Exception as e:
            health_status["issues"].append(f"Selenium版本检查失败: {str(e)}")
        
        # 检查测试图片
        default_image = os.path.join(e2e_service.test_data_dir, "disease_sample.jpg")
        if not os.path.exists(default_image):
            health_status["issues"].append(f"默认测试图片不存在: {default_image}")
        
        # 总体健康状态
        health_status["overall_status"] = "HEALTHY" if len(health_status["issues"]) == 0 else "ISSUES"
        
        return jsonify({
            "success": True,
            "data": health_status,
            "message": f"环境检查完成，状态: {health_status['overall_status']}"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"环境检查失败: {str(e)}"
        }), 500

@system_test_bp.route('/system/test/e2e/screenshots', methods=['GET'])
def list_test_screenshots():
    """
    获取测试截图列表
    """
    try:
        e2e_service = E2ETestService()
        screenshot_dir = e2e_service.screenshot_dir
        
        if not os.path.exists(screenshot_dir):
            return jsonify({
                "success": True,
                "data": {
                    "screenshots": [],
                    "count": 0
                },
                "message": "截图目录不存在"
            })
        
        screenshots = []
        for filename in os.listdir(screenshot_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(screenshot_dir, filename)
                file_stats = os.stat(filepath)
                
                screenshots.append({
                    "filename": filename,
                    "filepath": filepath,
                    "size": file_stats.st_size,
                    "created_time": file_stats.st_ctime,
                    "modified_time": file_stats.st_mtime
                })
        
        # 按修改时间排序（最新的在前）
        screenshots.sort(key=lambda x: x['modified_time'], reverse=True)
        
        return jsonify({
            "success": True,
            "data": {
                "screenshots": screenshots,
                "count": len(screenshots),
                "directory": screenshot_dir
            },
            "message": f"找到 {len(screenshots)} 个截图文件"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取截图列表失败: {str(e)}"
        }), 500

@system_test_bp.route('/system/test/e2e/cleanup', methods=['POST'])
def cleanup_test_files():
    """
    清理测试文件
    
    请求体格式：
    {
        "cleanup_types": ["screenshots", "logs", "temp_files"],
        "keep_recent": 5  // 保留最近的N个文件
    }
    """
    try:
        data = request.get_json() or {}
        cleanup_types = data.get('cleanup_types', ['screenshots'])
        keep_recent = data.get('keep_recent', 5)
        
        cleanup_results = {
            "cleaned_files": [],
            "errors": []
        }
        
        e2e_service = E2ETestService()
        
        if 'screenshots' in cleanup_types:
            try:
                screenshot_dir = e2e_service.screenshot_dir
                if os.path.exists(screenshot_dir):
                    # 获取所有截图文件
                    screenshot_files = []
                    for filename in os.listdir(screenshot_dir):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                            filepath = os.path.join(screenshot_dir, filename)
                            mtime = os.path.getmtime(filepath)
                            screenshot_files.append((filepath, mtime))
                    
                    # 按修改时间排序，保留最新的
                    screenshot_files.sort(key=lambda x: x[1], reverse=True)
                    files_to_delete = screenshot_files[keep_recent:]
                    
                    for filepath, _ in files_to_delete:
                        try:
                            os.remove(filepath)
                            cleanup_results["cleaned_files"].append(filepath)
                        except Exception as e:
                            cleanup_results["errors"].append(f"删除截图失败 {filepath}: {str(e)}")
                            
            except Exception as e:
                cleanup_results["errors"].append(f"清理截图目录失败: {str(e)}")
        
        if 'temp_files' in cleanup_types:
            try:
                # 清理临时目录
                temp_dir = "temp"
                if os.path.exists(temp_dir):
                    temp_files = []
                    for filename in os.listdir(temp_dir):
                        if filename.startswith('test_'):
                            filepath = os.path.join(temp_dir, filename)
                            mtime = os.path.getmtime(filepath)
                            temp_files.append((filepath, mtime))
                    
                    temp_files.sort(key=lambda x: x[1], reverse=True)
                    files_to_delete = temp_files[keep_recent:]
                    
                    for filepath, _ in files_to_delete:
                        try:
                            os.remove(filepath)
                            cleanup_results["cleaned_files"].append(filepath)
                        except Exception as e:
                            cleanup_results["errors"].append(f"删除临时文件失败 {filepath}: {str(e)}")
                            
            except Exception as e:
                cleanup_results["errors"].append(f"清理临时文件失败: {str(e)}")
        
        return jsonify({
            "success": True,
            "data": cleanup_results,
            "message": f"清理完成，删除了 {len(cleanup_results['cleaned_files'])} 个文件"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"清理操作失败: {str(e)}"
        }), 500

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