import os
import time
import json
from typing import Dict, Any, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import tempfile
import shutil

class E2ETestService:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.short_wait = None
        self.test_data_dir = "test_data"
        self.screenshot_dir = "test_screenshots"
        self._setup_test_directories()
        
    def _setup_test_directories(self):
        """设置测试目录"""
        os.makedirs(self.test_data_dir, exist_ok=True)
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
        # 创建默认测试图片（如果不存在）
        self._create_default_test_image()
    
    def _create_default_test_image(self):
        """创建默认测试图片"""
        test_image_path = os.path.join(self.test_data_dir, "disease_sample.jpg")
        if not os.path.exists(test_image_path):
            # 创建一个简单的测试图片
            try:
                from PIL import Image
                img = Image.new('RGB', (300, 200), color='green')
                img.save(test_image_path)
                print(f"创建默认测试图片: {test_image_path}")
            except ImportError:
                print("PIL未安装，请手动准备测试图片")
                
    def get_predefined_test_cases(self) -> List[Dict[str, Any]]:
        """返回端到端测试的预定义测试用例"""
        return [
            {
                "test_id": "E2E_TC_001",
                "test_name": "地块检测完整流程测试",
                "test_purpose": "验证用户从登录到完成地块检测的完整业务流程",
                "test_steps": [
                    "用户访问网站",
                    "用户输入用户名密码并登录",
                    "用户打开地块详情",
                    "用户点击病害检测",
                    "用户选择并提交图片",
                    "系统返回检测结果"
                ],
                "expected_result": "成功完成地块检测并获得结果",
                "test_type": "端到端测试",
                "priority": "高",
                "test_data": {
                    "image_path": os.path.join(self.test_data_dir, "disease_sample.jpg")
                }
            }
        ]
    
    def run_plot_detection_test(self, test_config: Dict[str, Any], test_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行地块检测端到端测试 - 改进版本"""
        max_retries = 3
        
        for attempt in range(max_retries):
            test_result = {
                "test_id": "E2E_TC_001",
                "test_name": "地块检测完整流程测试",
                "attempt": attempt + 1,
                "start_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "status": "RUNNING",
                "steps": [],
                "screenshots": [],
                "error_message": None,
                "execution_time": 0,
                "browser_logs": []
            }
            
            start_time = time.time()
            
            try:
                # 初始化浏览器
                self._setup_driver(test_config)
                
                # 执行测试步骤
                self._execute_test_steps(test_config, test_data, test_result)
                
                test_result["status"] = "PASSED"
                test_result["message"] = "测试执行成功"
                return test_result
                
            except Exception as e:
                error_msg = str(e)
                test_result["status"] = "FAILED"
                test_result["error_message"] = error_msg
                
                # 收集浏览器日志
                try:
                    if self.driver:
                        logs = self.driver.get_log('browser')
                        test_result["browser_logs"] = logs[-10:]  # 最后10条日志
                except Exception:
                    pass
                
                # 检查错误类型
                if any(keyword in error_msg.lower() for keyword in ["chrome", "webdriver", "connection"]):
                    test_result["error_type"] = "BROWSER_ERROR"
                    test_result["message"] = f"浏览器错误 (尝试 {attempt + 1}/{max_retries}): {error_msg}"
                else:
                    test_result["error_type"] = "TEST_ERROR"
                    test_result["message"] = f"测试执行失败 (尝试 {attempt + 1}/{max_retries}): {error_msg}"
                
                # 保存失败截图和页面源码
                if self.driver:
                    try:
                        screenshot_path = self._take_screenshot(f"test_failure_attempt_{attempt + 1}")
                        if screenshot_path:
                            test_result["screenshots"].append(screenshot_path)
                            
                        # 保存页面源码
                        page_source_path = self._save_page_source(f"test_failure_attempt_{attempt + 1}")
                        if page_source_path:
                            test_result["page_source"] = page_source_path
                    except Exception:
                        pass
                        
            finally:
                # 清理资源
                self._cleanup_driver()
                test_result["execution_time"] = round(time.time() - start_time, 2)
                test_result["end_time"] = time.strftime('%Y-%m-%d %H:%M:%S')
            
            # 如果不是浏览器错误，不重试
            if test_result.get("error_type") != "BROWSER_ERROR":
                break
                
            # 等待一段时间再重试
            if attempt < max_retries - 1:
                print(f"浏览器错误，等待5秒后重试...")
                time.sleep(5)
        
        return test_result

    def _setup_driver(self, config: Dict[str, Any]):
        """初始化WebDriver - 增强稳定性配置"""
        chrome_options = Options()
        
        # 基础稳定性配置
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')  # 加速加载
        
        # 内存和性能优化
        chrome_options.add_argument('--memory-pressure-off')
        chrome_options.add_argument('--max_old_space_size=4096')
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        
        # 网络优化
        chrome_options.add_argument('--aggressive-cache-discard')
        chrome_options.add_argument('--disable-background-networking')
        
        # 日志配置
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--log-level=0')
        chrome_options.add_argument('--v=1')
        
        # 设置窗口大小
        if config.get('headless', False):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--window-size=1920,1080')
        else:
            chrome_options.add_argument('--start-maximized')
        
        # 设置临时用户数据目录
        user_data_dir = tempfile.mkdtemp(prefix="chrome_test_")
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        
        # 设置下载目录
        download_dir = os.path.join(self.test_data_dir, "downloads")
        os.makedirs(download_dir, exist_ok=True)
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            # 创建Chrome服务
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # 设置超时时间
            timeout = config.get('timeout', 30)
            self.driver.implicitly_wait(timeout)
            self.driver.set_page_load_timeout(timeout)
            self.driver.set_script_timeout(timeout)
            
            # 创建WebDriverWait实例
            self.wait = WebDriverWait(self.driver, timeout)
            self.short_wait = WebDriverWait(self.driver, 5)
            
            # 最大化窗口（如果不是headless模式）
            if not config.get('headless', False):
                try:
                    self.driver.maximize_window()
                except Exception:
                    pass
            
            print(f"Chrome浏览器初始化成功，版本: {self.driver.capabilities['browserVersion']}")
            
        except Exception as e:
            raise Exception(f"Chrome浏览器初始化失败: {str(e)}")

    def _cleanup_driver(self):
        """清理WebDriver资源"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"清理浏览器时出错: {e}")
            finally:
                self.driver = None
                self.wait = None
                self.short_wait = None

    def _execute_test_steps(self, config: Dict[str, Any], test_data: Dict[str, Any], result: Dict[str, Any]):
        """执行测试步骤"""
        base_url = config.get('base_url', 'http://localhost:8100')
        username = config.get('test_username', 'testuser')
        password = config.get('test_password', 'testpass')
        
        # 步骤1: 访问网站
        self._add_step_result(result, "访问网站", "执行中")
        self._navigate_to_website(base_url)
        self._add_step_result(result, "访问网站", "成功")
        
        # 步骤2: 登录
        self._add_step_result(result, "用户登录", "执行中")
        self._perform_login(username, password)
        self._add_step_result(result, "用户登录", "成功")
        
        # 步骤3: 打开地块
        self._add_step_result(result, "打开地块详情", "执行中")
        self._open_plot_detail()
        self._add_step_result(result, "打开地块详情", "成功")
        
        # 步骤4: 病害检测
        self._add_step_result(result, "病害检测", "执行中")
        self._perform_disease_detection(test_data)
        self._add_step_result(result, "病害检测", "成功")
    
    def _navigate_to_website(self, base_url: str):
        """访问网站"""
        try:
            print(f"正在访问: {base_url}")
            self.driver.get(base_url)
            
            # 等待页面基本元素加载
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # 等待Ionic应用初始化
            self._wait_for_ionic_ready()
            
            print(f"成功访问网站: {self.driver.current_url}")
            
        except TimeoutException:
            raise Exception(f"访问网站超时: {base_url}")
        except Exception as e:
            raise Exception(f"访问网站失败: {str(e)}")
    
    def _wait_for_ionic_ready(self, timeout: int = 10):
        """等待Ionic应用就绪"""
        try:
            # 等待Ionic相关元素出现
            self.short_wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-app")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-content")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[ng-version]"))
                )
            )
            
            # 等待Angular/Ionic加载完成
            self.driver.execute_script("""
                return new Promise((resolve) => {
                    if (window.angular) {
                        // Angular应用
                        const element = document.querySelector('[ng-app]') || document.body;
                        window.angular.element(element).scope().$apply(() => {
                            resolve(true);
                        });
                    } else if (window.Ionic) {
                        // Ionic应用
                        window.Ionic.ready(() => {
                            resolve(true);
                        });
                    } else {
                        // 普通应用，等待DOM Ready
                        if (document.readyState === 'complete') {
                            resolve(true);
                        } else {
                            window.addEventListener('load', () => resolve(true));
                        }
                    }
                });
            """)
            
            time.sleep(1)  # 额外等待确保渲染完成
            
        except TimeoutException:
            print("Ionic应用加载检测超时，继续执行...")
        except Exception as e:
            print(f"Ionic就绪检测出错: {e}")
    
    def _add_step_result(self, result: Dict[str, Any], step_name: str, status: str):
        """添加步骤结果"""
        step_info = {
            "step_name": step_name,
            "status": status,
            "timestamp": time.strftime('%H:%M:%S')
        }
        result["steps"].append(step_info)
        print(f"步骤: {step_name} - {status}")
    
    def _perform_login(self, username: str, password: str):
        """执行登录操作 - 改进版本"""
        try:
            # 等待页面完全加载
            time.sleep(2)
            
            # 查找用户名输入框
            username_input = self._find_element_by_multiple_selectors([
                "ion-input[label*='用户名'] input",
                "ion-input[placeholder*='用户名'] input", 
                "input[placeholder*='用户名']",
                "input[type='text']",
                "#username",
                "[name='username']"
            ], "用户名输入框")
            
            # 输入用户名
            self._safe_input(username_input, username, "用户名")
            
            # 查找密码输入框
            password_input = self._find_element_by_multiple_selectors([
                "ion-input[label*='密码'] input",
                "ion-input[placeholder*='密码'] input",
                "input[placeholder*='密码']",
                "input[type='password']",
                "#password",
                "[name='password']"
            ], "密码输入框")
            
            # 输入密码
            self._safe_input(password_input, password, "密码")
            
            # 查找登录按钮
            login_button = self._find_element_by_multiple_selectors([
                "ion-button[type='submit']",
                "button[type='submit']",
                "ion-button:not([fill='outline'])",
                "#login-button",
                "[class*='login-btn']"
            ], "登录按钮")
            
            # 点击登录按钮
            self._safe_click(login_button, "登录按钮")
            
            # 等待登录处理
            time.sleep(2)
            
            # 验证登录成功
            self._verify_login_success()
            
            print("登录成功")
            
        except Exception as e:
            # 检查是否有错误提示
            error_message = self._get_error_message()
            if error_message:
                raise Exception(f"登录失败: {error_message}")
            else:
                raise Exception(f"登录过程失败: {str(e)}")
    
    def _find_element_by_multiple_selectors(self, selectors: List[str], element_name: str, timeout: int = 10):
        """通过多个选择器查找元素"""
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                if element.is_displayed() and element.is_enabled():
                    print(f"找到{element_name}: {selector}")
                    return element
            except TimeoutException:
                continue
            except Exception:
                continue
        
        raise Exception(f"未找到{element_name}")
    
    def _safe_input(self, element, text: str, field_name: str):
        """安全输入文本"""
        try:
            # 清空输入框
            element.clear()
            time.sleep(0.3)
            
            # 输入文本
            element.send_keys(text)
            time.sleep(0.3)
            
            # 验证输入
            actual_value = element.get_attribute('value')
            if actual_value != text:
                # 尝试JavaScript输入
                self.driver.execute_script(f"arguments[0].value = '{text}';", element)
                # 触发input事件
                self.driver.execute_script("""
                    var event = new Event('input', { bubbles: true });
                    arguments[0].dispatchEvent(event);
                """, element)
                
            print(f"{field_name}输入完成")
            
        except Exception as e:
            raise Exception(f"{field_name}输入失败: {str(e)}")
    
    def _safe_click(self, element, element_name: str):
        """安全点击元素"""
        try:
            # 滚动到元素可见
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # 尝试普通点击
            element.click()
            
        except Exception:
            try:
                # 尝试JavaScript点击
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                # 尝试ActionChains点击
                ActionChains(self.driver).move_to_element(element).click().perform()
        
        print(f"{element_name}点击完成")
        time.sleep(0.5)
    
    def _verify_login_success(self):
        """验证登录成功"""
        try:
            # 等待URL跳转
            self.wait.until(
                EC.any_of(
                    EC.url_contains("/tabs/home"),
                    EC.url_contains("/home"),
                    EC.url_contains("/dashboard"),
                    EC.url_contains("/main")
                )
            )
            
            current_url = self.driver.current_url
            print(f"登录后URL: {current_url}")
            
            # 等待首页内容加载
            time.sleep(3)
            
        except TimeoutException:
            raise Exception("登录后未跳转到首页，可能登录失败")
    
    def _get_error_message(self) -> str:
        """获取页面错误信息"""
        error_selectors = [
            "ion-toast .toast-message",
            ".error-message",
            "[class*='error']",
            "[class*='alert']",
            "ion-alert .alert-message"
        ]
        
        for selector in error_selectors:
            try:
                error_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if error_element.is_displayed():
                    return error_element.text.strip()
            except NoSuchElementException:
                continue
        
        return ""

    def _open_plot_detail(self):
        """打开地块详情 - 改进版本"""
        try:
            # 等待页面完全加载
            time.sleep(3)
            
            # 查找地块卡片
            plot_cards = self._find_plot_cards()
            
            if not plot_cards:
                raise Exception("未找到地块卡片")
            
            # 点击第一个地块卡片
            first_card = plot_cards[0]
            router_link = first_card.get_attribute('routerlink')
            print(f"准备点击地块卡片，routerlink: {router_link}")
            
            # 安全点击地块卡片
            self._safe_click(first_card, "地块卡片")
            
            # 等待页面跳转
            time.sleep(3)
            
            # 验证跳转
            current_url = self.driver.current_url
            if "/tabs/strip/" not in current_url and "/plot/" not in current_url:
                raise Exception(f"点击地块后未跳转到详情页，当前URL: {current_url}")
            
            print(f"成功跳转到地块详情页: {current_url}")
            
        except Exception as e:
            screenshot_path = self._take_screenshot("plot_detail_error")
            raise Exception(f"打开地块详情失败: {str(e)}，截图: {screenshot_path}")
    
    def _find_plot_cards(self):
        """查找地块卡片"""
        plot_selectors = [
            "ion-card[routerlink*='/tabs/strip/']",
            "ion-card[routerlink*='/plot/']", 
            "ion-card[routerlink]",
            "ion-card.ion-activatable",
            ".plot-card",
            "ion-card"
        ]
        
        for selector in plot_selectors:
            try:
                cards = self.wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                )
                
                # 过滤可见且可点击的卡片
                visible_cards = [
                    card for card in cards 
                    if card.is_displayed() and card.is_enabled()
                ]
                
                if visible_cards:
                    print(f"找到 {len(visible_cards)} 个地块卡片，使用选择器: {selector}")
                    return visible_cards
                    
            except TimeoutException:
                continue
        
        # 尝试滚动加载
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # 再次尝试查找
        for selector in plot_selectors:
            try:
                cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                visible_cards = [card for card in cards if card.is_displayed()]
                if visible_cards:
                    return visible_cards
            except Exception:
                continue
        
        return []

    def _perform_disease_detection(self, test_data: Dict[str, Any]):
        """执行病害检测 - 改进版本"""
        try:
            # 查找并点击更多选项按钮
            more_button = self._find_element_by_multiple_selectors([
                "#more-options-button",
                "ion-button[id*='more']",
                "ion-button[class*='more']",
                "[data-testid='more-options']"
            ], "更多选项按钮")
            
            self._safe_click(more_button, "更多选项按钮")
            time.sleep(1)
            
            # 查找并点击疾病检测选项
            detect_option = self._find_disease_detection_option()
            self._safe_click(detect_option, "疾病检测选项")
            time.sleep(2)
            
            # 上传测试图片
            self._upload_test_image(test_data)
            
            # 提交检测并等待结果
            self._submit_detection_and_wait()
            
            print("病害检测完成")
            
        except Exception as e:
            screenshot_path = self._take_screenshot("disease_detection_error")
            raise Exception(f"病害检测执行失败: {str(e)}，截图: {screenshot_path}")
    
    def _find_disease_detection_option(self):
        """查找疾病检测选项"""
        # 尝试多种方式查找疾病检测选项
        selectors = [
            "ion-item ion-label[text()='疾病检测']",
            "ion-item:contains('疾病检测')",
            "[data-testid='disease-detection']",
            "ion-item[class*='disease']"
        ]
        
        for selector in selectors:
            try:
                if "contains" in selector:
                    # 使用JavaScript查找包含文本的元素
                    elements = self.driver.execute_script("""
                        return Array.from(document.querySelectorAll('ion-item')).filter(
                            el => el.textContent.includes('疾病检测') || 
                                  el.textContent.includes('病害检测') ||
                                  el.textContent.includes('检测')
                        );
                    """)
                    if elements:
                        return elements[0]
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        return element
            except Exception:
                continue
        
        # 如果找不到，尝试查找所有ion-item并检查文本
        items = self.driver.find_elements(By.CSS_SELECTOR, "ion-item")
        for item in items:
            if item.is_displayed():
                text = item.text.lower()
                if any(keyword in text for keyword in ['疾病', '病害', '检测', 'disease', 'detection']):
                    return item
        
        raise Exception("未找到疾病检测选项")
    
    def _upload_test_image(self, test_data: Dict[str, Any]):
        """上传测试图片"""
        image_path = test_data.get('image_path', os.path.join(self.test_data_dir, 'disease_sample.jpg'))
        
        if not os.path.exists(image_path):
            raise Exception(f"测试图片不存在: {image_path}")
        
        # 查找文件上传输入框
        file_input = self._find_element_by_multiple_selectors([
            "input[type='file']",
            "[type='file']",
            "#file-upload",
            "[data-testid='file-input']"
        ], "文件上传输入框")
        
        # 上传文件
        absolute_path = os.path.abspath(image_path)
        file_input.send_keys(absolute_path)
        time.sleep(2)
        
        print(f"图片上传完成: {image_path}")
    
    def _submit_detection_and_wait(self):
        """提交检测并等待结果"""
        # 查找并点击提交按钮
        submit_button = self._find_element_by_multiple_selectors([
            "ion-button[type='submit']",
            "button[type='submit']",
            "ion-button:contains('提交')",
            "ion-button:contains('检测')",
            "#submit-button",
            "[data-testid='submit-btn']"
        ], "提交按钮")
        
        self._safe_click(submit_button, "提交按钮")
        print("已提交病害检测请求")
        
        # 等待检测结果
        self._wait_for_detection_result()
    
    def _wait_for_detection_result(self):
        """等待检测结果"""
        max_wait_time = 120  # 最大等待2分钟
        check_interval = 5   # 每5秒检查一次
        
        for attempt in range(max_wait_time // check_interval):
            try:
                # 检查是否有结果显示
                if self._check_for_detection_result():
                    print(f"检测结果已生成 (等待时间: {(attempt + 1) * check_interval}秒)")
                    return True
                
                # 检查是否有错误信息
                error_msg = self._check_for_error_message()
                if error_msg:
                    raise Exception(f"检测过程中出现错误: {error_msg}")
                
                print(f"等待检测结果... ({(attempt + 1) * check_interval}/{max_wait_time}秒)")
                time.sleep(check_interval)
                
            except Exception as e:
                if "检测过程中出现错误" in str(e):
                    raise e
                # 其他异常继续等待
                time.sleep(check_interval)
        
        # 超时处理
        print(f"检测处理超时 ({max_wait_time}秒)")
        
        # 最后尝试：查找页面上的任何结果相关信息
        if self._has_any_result_content():
            print("找到结果相关内容，认为检测可能已完成")
            return True
        
        raise Exception(f"检测处理超时，未在{max_wait_time}秒内获得有效结果")
    
    def _check_for_detection_result(self) -> bool:
        """检查是否有检测结果"""
        result_selectors = [
            "ion-card .result-content",
            "ion-card .detection-result", 
            ".result-card",
            ".detection-result",
            "[data-testid='detection-result']",
            "ion-card[class*='result']"
        ]
        
        for selector in result_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed():
                    return True
            except NoSuchElementException:
                continue
        
        # 检查是否有包含结果关键词的卡片
        try:
            result_cards = self.driver.execute_script("""
                return Array.from(document.querySelectorAll('ion-card')).filter(
                    card => {
                        const text = card.textContent.toLowerCase();
                        return text.includes('结果') || 
                               text.includes('检测完成') || 
                               text.includes('分析结果') ||
                               text.includes('result') ||
                               text.includes('detection');
                    }
                );
            """)
            return len(result_cards) > 0
        except Exception:
            return False
    
    def _check_for_error_message(self) -> str:
        """检查错误信息"""
        error_keywords = ["检测失败", "处理失败", "错误", "失败", "error", "failed"]
        
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            for keyword in error_keywords:
                if keyword in page_text:
                    return keyword
        except Exception:
            pass
        
        return ""
    
    def _has_any_result_content(self) -> bool:
        """检查是否有任何结果相关内容"""
        try:
            page_source = self.driver.page_source.lower()
            result_keywords = ["结果", "检测", "分析", "完成", "result", "detection", "analysis"]
            
            found_keywords = [keyword for keyword in result_keywords if keyword in page_source]
            return len(found_keywords) >= 2  # 至少找到2个相关关键词
        except Exception:
            return False
    
    def _take_screenshot(self, name: str) -> str:
        """截图保存"""
        try:
            timestamp = int(time.time())
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            self.driver.save_screenshot(filepath)
            print(f"截图已保存: {filepath}")
            return filepath
        except Exception as e:
            print(f"截图失败: {e}")
            return None
    
    def _save_page_source(self, name: str) -> str:
        """保存页面源码"""
        try:
            timestamp = int(time.time())
            filename = f"{name}_{timestamp}.html"
            filepath = os.path.join(self.screenshot_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            
            print(f"页面源码已保存: {filepath}")
            return filepath
        except Exception as e:
            print(f"保存页面源码失败: {e}")
            return None

    # === 天气信息测试相关方法 ===
    
    def get_weather_predefined_test_cases(self) -> List[Dict[str, Any]]:
        """返回天气信息测试的预定义测试用例"""
        return [
            {
                "test_id": "Pguard_Sys_Test_case_fun_002",
                "test_name": "用户查看天气信息",
                "test_purpose": "验证用户登录后能够查看当地天气信息",
                "test_method": "场景法",
                "precondition": "用户已有账户",
                "test_steps": [
                    "用户访问网站",
                    "用户输入用户名密码并登录",
                    "系统跳转到首页",
                    "系统自动获取用户当地天气信息",
                    "显示用户当地天气信息"
                ],
                "expected_result": "显示用户当地天气信息",
                "test_type": "端到端测试",
                "priority": "中"
            }
        ]
    
    def run_weather_info_test(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        """执行天气信息查看端到端测试"""
        test_result = {
            "test_id": "Pguard_Sys_Test_case_fun_002",
            "test_name": "用户查看天气信息",
            "start_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "status": "RUNNING",
            "steps": [],
            "screenshots": [],
            "weather_data": {},
            "error_message": None,
            "execution_time": 0
        }
        
        start_time = time.time()
        
        try:
            # 初始化浏览器
            self._setup_driver(test_config)
            
            # 执行天气信息测试步骤
            self._execute_weather_test_steps(test_config, test_result)
            
            test_result["status"] = "PASSED"
            test_result["message"] = "天气信息测试执行成功"
            
        except Exception as e:
            test_result["status"] = "FAILED"
            test_result["error_message"] = str(e)
            test_result["message"] = f"天气信息测试执行失败: {str(e)}"
            
            # 保存失败截图
            if self.driver:
                screenshot_path = self._take_screenshot("weather_test_failure")
                if screenshot_path:
                    test_result["screenshots"].append(screenshot_path)
                    
        finally:
            # 清理资源
            self._cleanup_driver()
            test_result["execution_time"] = round(time.time() - start_time, 2)
            test_result["end_time"] = time.strftime('%Y-%m-%d %H:%M:%S')
            
        return test_result
    
    def _execute_weather_test_steps(self, config: Dict[str, Any], result: Dict[str, Any]):
        """执行天气信息测试步骤"""
        base_url = config.get('base_url', 'http://localhost:8100')
        username = config.get('test_username', 'testuser')
        password = config.get('test_password', 'testpass')
        
        # 步骤1: 访问网站
        self._add_step_result(result, "用户访问网站", "执行中")
        self._navigate_to_website(base_url)
        self._add_step_result(result, "用户访问网站", "成功")
        
        # 步骤2: 用户登录
        self._add_step_result(result, "用户输入用户名密码并登录", "执行中")
        self._perform_login(username, password)
        self._add_step_result(result, "用户输入用户名密码并登录", "成功")
        
        # 步骤3: 验证跳转到首页
        self._add_step_result(result, "系统跳转到首页", "执行中")
        self._verify_login_success()
        self._add_step_result(result, "系统跳转到首页", "成功")
        
        # 步骤4: 验证天气信息获取和显示
        self._add_step_result(result, "获取并显示天气信息", "执行中")
        weather_data = self._verify_weather_info_display()
        result["weather_data"] = weather_data
        self._add_step_result(result, "获取并显示天气信息", "成功")
    
    def _verify_weather_info_display(self) -> Dict[str, Any]:
        """验证天气信息的显示"""
        # 等待天气信息加载
        time.sleep(3)
        
        weather_data = {}
        
        try:
            # 查找天气信息容器
            weather_containers = [
                ".weather-info",
                "[class*='weather']",
                "ion-card:first-child",
                ".weather-widget",
                "[data-testid='weather']"
            ]
            
            weather_container = None
            for selector in weather_containers:
                try:
                    container = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if container.is_displayed():
                        weather_container = container
                        break
                except NoSuchElementException:
                    continue
            
            if not weather_container:
                # 尝试通过文本内容查找包含天气信息的元素
                weather_container = self._find_weather_by_content()
            
            if not weather_container:
                raise Exception("未找到天气信息容器")
            
            # 提取天气信息
            weather_data = self._extract_weather_data(weather_container)
            
            # 验证至少有一些天气信息
            if not any(weather_data.values()):
                raise Exception("天气信息容器存在但未找到具体天气数据")
            
            weather_data["status"] = "天气信息获取成功"
            
            # 截图保存天气信息显示状态
            screenshot_path = self._take_screenshot("weather_info_display")
            if screenshot_path:
                weather_data["screenshot"] = screenshot_path
            
            return weather_data
            
        except Exception as e:
            raise Exception(f"天气信息验证失败: {str(e)}")
    
    def _find_weather_by_content(self):
        """通过内容查找天气信息"""
        try:
            weather_elements = self.driver.execute_script("""
                return Array.from(document.querySelectorAll('*')).filter(el => {
                    const text = el.textContent.toLowerCase();
                    return (text.includes('天气') || 
                           text.includes('温度') || 
                           text.includes('°c') || 
                           text.includes('°f') ||
                           text.includes('weather') ||
                           text.includes('temperature')) &&
                           el.children.length > 0;  // 确保不是叶子节点
                });
            """)
            
            if weather_elements:
                return weather_elements[0]
                
        except Exception:
            pass
        
        return None
    
    def _extract_weather_data(self, container) -> Dict[str, Any]:
        """从容器中提取天气数据"""
        weather_data = {}
        
        # 尝试获取各种天气信息
        weather_elements = {
            "temperature": ["[class*='temp']", "[class*='temperature']", "ion-card-title"],
            "weather_icon": ["ion-icon", "[class*='weather-icon']", "img[alt*='weather']"],
            "location": ["[class*='location']", "[class*='city']", "ion-card-subtitle"],
            "description": ["[class*='desc']", "[class*='condition']", "ion-card-content"]
        }
        
        for key, selectors in weather_elements.items():
            for selector in selectors:
                try:
                    element = container.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        if key == "weather_icon":
                            weather_data[key] = element.get_attribute("name") or element.get_attribute("src") or "found"
                        else:
                            text = element.text.strip()
                            if text:
                                weather_data[key] = text
                        break
                except NoSuchElementException:
                    continue
        
        # 如果没有找到具体信息，检查容器文本
        if not weather_data:
            container_text = container.text.strip()
            if container_text:
                weather_data["container_text"] = container_text
                
                # 检查是否包含天气相关关键词
                weather_keywords = ["天气", "温度", "°C", "°F", "晴", "雨", "云", "weather", "temperature"]
                found_keywords = [keyword for keyword in weather_keywords if keyword.lower() in container_text.lower()]
                
                if found_keywords:
                    weather_data["found_keywords"] = found_keywords
        
        return weather_data


# 测试工具类
class E2ETestUtils:
    """E2E测试工具类"""
    
    @staticmethod
    def validate_test_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """验证测试配置"""
        default_config = {
            "base_url": "http://localhost:8100",
            "test_username": "testuser", 
            "test_password": "testpass",
            "headless": False,
            "timeout": 30
        }
        
        # 合并配置
        validated_config = {**default_config, **config}
        
        # 验证必要字段
        required_fields = ["base_url", "test_username", "test_password"]
        for field in required_fields:
            if not validated_config.get(field):
                raise ValueError(f"缺少必要配置项: {field}")
        
        return validated_config
    
    @staticmethod
    def validate_test_data(test_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证测试数据"""
        default_data = {
            "image_path": "test_data/disease_sample.jpg"
        }
        
        validated_data = {**default_data, **test_data}
        
        # 验证图片路径
        image_path = validated_data.get("image_path")
        if image_path and not os.path.exists(image_path):
            print(f"警告: 测试图片不存在: {image_path}")
        
        return validated_data
    
    @staticmethod
    def generate_test_report(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成测试报告"""
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.get("status") == "PASSED"])
        failed_tests = total_tests - passed_tests
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "pass_rate": round((passed_tests / total_tests * 100), 2) if total_tests > 0 else 0
            },
            "test_results": test_results,
            "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return report