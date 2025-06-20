"""
E2E测试工具类
"""
import os
import time
from typing import Dict, Any, List

from app.static.system_test import (
    DEFAULT_TEST_CONFIG, 
    TEST_DIRECTORIES, 
    DEFAULT_TEST_IMAGE
)


class E2ETestUtils:
    """E2E测试工具类"""
    
    @staticmethod
    def validate_test_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证测试配置
        
        Args:
            config: 测试配置字典
            
        Returns:
            验证后的配置字典
            
        Raises:
            ValueError: 当缺少必要配置项时
        """
        # 合并默认配置和用户配置
        validated_config = {**DEFAULT_TEST_CONFIG, **config}
        
        # 验证必要字段
        required_fields = ["base_url", "test_username", "test_password"]
        for field in required_fields:
            if not validated_config.get(field):
                raise ValueError(f"缺少必要配置项: {field}")
        
        # 验证数据类型
        if not isinstance(validated_config.get("headless"), bool):
            validated_config["headless"] = bool(validated_config.get("headless", False))
        
        if not isinstance(validated_config.get("timeout"), (int, float)):
            try:
                validated_config["timeout"] = float(validated_config.get("timeout", 30))
            except (ValueError, TypeError):
                validated_config["timeout"] = 30
        
        return validated_config
    
    @staticmethod
    def validate_test_data(test_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证测试数据
        
        Args:
            test_data: 测试数据字典
            
        Returns:
            验证后的测试数据字典
        """
        # 设置默认测试数据
        default_data = {
            "image_path": os.path.join(TEST_DIRECTORIES["test_data"], DEFAULT_TEST_IMAGE["filename"])
        }
        
        # 合并默认数据和用户数据
        validated_data = {**default_data, **test_data}
        
        # 验证图片路径
        image_path = validated_data.get("image_path")
        if image_path and not os.path.exists(image_path):
            print(f"[警告] 测试图片不存在: {image_path}")
            # 尝试创建默认测试图片
            E2ETestUtils._create_default_test_image(image_path)
        
        return validated_data
    
    @staticmethod
    def _create_default_test_image(image_path: str) -> bool:
        """
        创建默认测试图片
        
        Args:
            image_path: 图片路径
            
        Returns:
            是否创建成功
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # 尝试使用PIL创建图片
            try:
                from PIL import Image
                
                # 创建图片
                img = Image.new('RGB', DEFAULT_TEST_IMAGE["size"], color=DEFAULT_TEST_IMAGE["color"])
                img.save(image_path)
                print(f"[调试] 创建默认测试图片: {image_path}")
                return True
                
            except ImportError:
                # PIL不可用，创建简单的文本文件作为占位符
                placeholder_path = image_path + ".txt"
                with open(placeholder_path, 'w', encoding='utf-8') as f:
                    f.write("测试图片占位符 - 请手动准备测试图片\n")
                    f.write(f"预期图片路径: {image_path}\n")
                    f.write(f"图片尺寸: {DEFAULT_TEST_IMAGE['size']}\n")
                    f.write(f"图片颜色: {DEFAULT_TEST_IMAGE['color']}\n")
                print(f"[调试] PIL不可用，创建测试图片占位符: {placeholder_path}")
                return False
                
        except Exception as e:
            print(f"[调试] 创建默认测试图片失败: {e}")
            return False
    
    @staticmethod
    def generate_test_report(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成测试报告
        
        Args:
            test_results: 测试结果列表
            
        Returns:
            测试报告字典
        """
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.get("status") == "PASSED"])
        failed_tests = total_tests - passed_tests
        
        # 计算通过率
        pass_rate = round((passed_tests / total_tests * 100), 2) if total_tests > 0 else 0
        
        # 统计执行时间
        total_execution_time = sum(r.get("execution_time", 0) for r in test_results)
        avg_execution_time = round(total_execution_time / total_tests, 2) if total_tests > 0 else 0
        
        # 统计重试次数
        total_retries = sum(r.get("attempt", 1) - 1 for r in test_results)
        
        # 分类失败的测试
        failed_by_type = {}
        for result in test_results:
            if result.get("status") == "FAILED":
                error_type = E2ETestUtils._categorize_error(result.get("error_message", ""))
                failed_by_type[error_type] = failed_by_type.get(error_type, 0) + 1
        
        return {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "pass_rate": pass_rate,
                "total_execution_time": round(total_execution_time, 2),
                "avg_execution_time": avg_execution_time,
                "total_retries": total_retries
            },
            "failure_analysis": {
                "failed_by_type": failed_by_type
            },
            "test_results": test_results,
            "generated_at": time.strftime('%Y-%m-%d %H:%M:%S'),
            "report_version": "1.0"
        }
    
    @staticmethod
    def _categorize_error(error_message: str) -> str:
        """
        对错误信息进行分类
        
        Args:
            error_message: 错误信息
            
        Returns:
            错误类型
        """
        if not error_message:
            return "UNKNOWN"
        
        error_message = error_message.lower()
        
        # 浏览器相关错误
        if any(keyword in error_message for keyword in ["chrome", "browser", "driver", "webdriver"]):
            return "BROWSER_ERROR"
        
        # 网络相关错误
        if any(keyword in error_message for keyword in ["network", "connection", "timeout", "网络", "连接", "超时"]):
            return "NETWORK_ERROR"
        
        # 元素查找错误
        if any(keyword in error_message for keyword in ["element", "selector", "not found", "未找到", "无法找到"]):
            return "ELEMENT_ERROR"
        
        # 登录相关错误
        if any(keyword in error_message for keyword in ["login", "登录", "authentication", "认证"]):
            return "LOGIN_ERROR"
        
        # 上传相关错误
        if any(keyword in error_message for keyword in ["upload", "file", "上传", "文件"]):
            return "UPLOAD_ERROR"
        
        # 检测相关错误
        if any(keyword in error_message for keyword in ["detection", "检测", "result", "结果"]):
            return "DETECTION_ERROR"
        
        # 页面加载错误
        if any(keyword in error_message for keyword in ["page", "load", "页面", "加载"]):
            return "PAGE_LOAD_ERROR"
        
        return "OTHER_ERROR"
    
    @staticmethod
    def setup_test_directories():
        """设置测试目录"""
        for dir_path in TEST_DIRECTORIES.values():
            os.makedirs(dir_path, exist_ok=True)
            print(f"[调试] 确保目录存在: {dir_path}")
    
    @staticmethod
    def cleanup_test_files(keep_recent: int = 5):
        """
        清理测试文件
        
        Args:
            keep_recent: 保留最近的文件数量
        """
        try:
            # 清理截图文件
            screenshot_dir = TEST_DIRECTORIES["screenshots"]
            if os.path.exists(screenshot_dir):
                screenshot_files = [
                    f for f in os.listdir(screenshot_dir) 
                    if f.endswith('.png')
                ]
                screenshot_files.sort(key=lambda x: os.path.getctime(os.path.join(screenshot_dir, x)), reverse=True)
                
                # 删除多余的截图文件
                for file_to_delete in screenshot_files[keep_recent:]:
                    file_path = os.path.join(screenshot_dir, file_to_delete)
                    os.remove(file_path)
                    print(f"[调试] 删除旧截图文件: {file_path}")
            
            # 清理测试数据文件（除了默认图片）
            test_data_dir = TEST_DIRECTORIES["test_data"]
            if os.path.exists(test_data_dir):
                default_image_name = DEFAULT_TEST_IMAGE["filename"]
                for file_name in os.listdir(test_data_dir):
                    if file_name != default_image_name and file_name.endswith('.tmp'):
                        file_path = os.path.join(test_data_dir, file_name)
                        os.remove(file_path)
                        print(f"[调试] 删除临时测试文件: {file_path}")
                        
        except Exception as e:
            print(f"[调试] 清理测试文件失败: {e}")
    
    @staticmethod
    def format_execution_time(seconds: float) -> str:
        """
        格式化执行时间
        
        Args:
            seconds: 秒数
            
        Returns:
            格式化后的时间字符串
        """
        if seconds < 60:
            return f"{seconds:.2f}秒"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            remaining_seconds = seconds % 60
            return f"{minutes}分{remaining_seconds:.1f}秒"
        else:
            hours = int(seconds // 3600)
            remaining_minutes = int((seconds % 3600) // 60)
            remaining_seconds = seconds % 60
            return f"{hours}小时{remaining_minutes}分{remaining_seconds:.1f}秒"
    
    @staticmethod
    def validate_browser_environment() -> Dict[str, Any]:
        """
        验证浏览器环境
        
        Returns:
            环境验证结果
        """
        validation_result = {
            "chrome_available": False,
            "chromedriver_available": False,
            "pil_available": False,
            "environment_ready": False,
            "recommendations": []
        }
        
        try:
            # 检查Chrome浏览器
            import subprocess
            try:
                result = subprocess.run(['google-chrome', '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    validation_result["chrome_available"] = True
                    validation_result["chrome_version"] = result.stdout.strip()
                else:
                    validation_result["recommendations"].append("请安装Google Chrome浏览器")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                validation_result["recommendations"].append("请安装Google Chrome浏览器")
            
            # 检查ChromeDriver
            try:
                from selenium import webdriver
                from selenium.webdriver.chrome.service import Service
                service = Service()
                validation_result["chromedriver_available"] = True
            except Exception:
                validation_result["recommendations"].append("请安装ChromeDriver")
            
            # 检查PIL
            try:
                from PIL import Image
                validation_result["pil_available"] = True
            except ImportError:
                validation_result["recommendations"].append("建议安装Pillow库以支持图片生成: pip install Pillow")
            
            # 综合判断环境是否就绪
            validation_result["environment_ready"] = (
                validation_result["chrome_available"] and 
                validation_result["chromedriver_available"]
            )
            
        except Exception as e:
            validation_result["error"] = str(e)
            validation_result["recommendations"].append("环境检查过程中出现错误")
        
        return validation_result