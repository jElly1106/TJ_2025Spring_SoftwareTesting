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

from app.static.system_test import (
    DEFAULT_TEST_CONFIG, CHROME_OPTIONS, HEADLESS_WINDOW_SIZE, MAXIMIZED_WINDOW,
    TEST_DIRECTORIES, DEFAULT_TEST_IMAGE, RETRY_CONFIG, WAIT_CONFIG,
    DETECTION_WAIT_CONFIG, SELECTORS, URL_VALIDATION, TEST_CASES_CONFIG,
    JAVASCRIPT_SCRIPTS
)

class E2ETestConfig:
    """E2E测试配置管理类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._set_defaults()
    
    def _set_defaults(self):
        for key, value in DEFAULT_TEST_CONFIG.items():
            if key not in self.config:
                self.config[key] = value
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
    
    def get_base_url(self) -> str:
        return self.config['base_url']
    
    def validate(self):
        required_fields = ["base_url", "test_username", "test_password"]
        for field in required_fields:
            if not self.config.get(field):
                raise ValueError(f"缺少必要配置项: {field}")

class E2ETestService:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.short_wait = None
        self.test_data_dir = TEST_DIRECTORIES["test_data"]
        self.screenshot_dir = TEST_DIRECTORIES["screenshots"]
        self._setup_test_directories()
        
    def _setup_test_directories(self):
        for dir_path in TEST_DIRECTORIES.values():
            os.makedirs(dir_path, exist_ok=True)
        self._create_default_test_image()
    
    def _create_default_test_image(self):
        test_image_path = os.path.join(self.test_data_dir, DEFAULT_TEST_IMAGE["filename"])
        if not os.path.exists(test_image_path):
            try:
                from PIL import Image
                img = Image.new('RGB', DEFAULT_TEST_IMAGE["size"], color=DEFAULT_TEST_IMAGE["color"])
                img.save(test_image_path)
            except ImportError:
                pass
                
    def get_predefined_test_cases(self) -> List[Dict[str, Any]]:
        test_case = TEST_CASES_CONFIG["plot_detection"].copy()
        test_case["test_data"] = {
            "image_path": os.path.join(self.test_data_dir, DEFAULT_TEST_IMAGE["filename"])
        }
        return [test_case]
    
    def run_plot_detection_test(self, test_config: Dict[str, Any], test_data: Dict[str, Any]) -> Dict[str, Any]:
        print(f"\n[测试开始] 地块检测测试")
        print(f"[配置] 基础URL: {test_config.get('base_url', '未设置')}")
        print(f"[配置] 用户名: {test_config.get('test_username', '未设置')}")
        print(f"[配置] 无头模式: {test_config.get('headless', False)}")
        
        config = E2ETestConfig(test_config)
        config.validate()
        
        for attempt in range(RETRY_CONFIG["max_retries"]):
            print(f"\n[重试] 第 {attempt + 1} 次尝试")
            
            test_result = {
                "test_id": TEST_CASES_CONFIG["plot_detection"]["test_id"],
                "test_name": TEST_CASES_CONFIG["plot_detection"]["test_name"],
                "attempt": attempt + 1,
                "start_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                "status": "RUNNING",
                "steps": [],
                "screenshots": [],
                "error_message": None,
                "execution_time": 0
            }
            
            start_time = time.time()
            
            try:
                print(f"[调试] 设置浏览器驱动")
                self._setup_driver(config.config)
                print(f"[调试] 开始执行测试步骤")
                self._execute_test_steps(config, test_data, test_result)
                test_result["status"] = "PASSED"
                test_result["message"] = "测试执行成功"
                print(f"\n[测试成功] 地块检测测试执行成功")
                return test_result
                
            except Exception as e:
                test_result["status"] = "FAILED"
                test_result["error_message"] = str(e)
                test_result["message"] = f"测试执行失败: {str(e)}"
                print(f"\n[测试失败] {str(e)}")
                
                if self.driver:
                    screenshot_path = self._take_screenshot(f"test_failure_attempt_{attempt + 1}")
                    if screenshot_path:
                        test_result["screenshots"].append(screenshot_path)
                        print(f"[调试] 失败截图已保存: {screenshot_path}")
                        
            finally:
                print(f"[调试] 清理浏览器驱动")
                self._cleanup_driver()
                test_result["execution_time"] = round(time.time() - start_time, 2)
                test_result["end_time"] = time.strftime('%Y-%m-%d %H:%M:%S')
                print(f"[调试] 本次尝试执行时间: {test_result['execution_time']}秒")
        
            if "browser" not in str(test_result.get("error_message", "")).lower():
                print(f"[调试] 非浏览器相关错误，停止重试")
                break
                
            if attempt < RETRY_CONFIG["max_retries"] - 1:
                print(f"[调试] 等待 {RETRY_CONFIG['retry_delay']} 秒后重试")
                time.sleep(RETRY_CONFIG["retry_delay"])
        
        print(f"\n[测试结束] 地块检测测试")
        return test_result

    def _setup_driver(self, config: Dict[str, Any]):
        chrome_options = Options()
        
        for option in CHROME_OPTIONS:
            chrome_options.add_argument(option)
        
        if config.get('headless', False):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument(HEADLESS_WINDOW_SIZE)
        else:
            chrome_options.add_argument(MAXIMIZED_WINDOW)
        
        user_data_dir = tempfile.mkdtemp(prefix="chrome_test_")
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        
        try:
            service = Service()
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            timeout = config.get('timeout', WAIT_CONFIG["implicit_wait"])
            self.driver.implicitly_wait(timeout)
            self.driver.set_page_load_timeout(WAIT_CONFIG["page_load_timeout"])
            
            self.wait = WebDriverWait(self.driver, timeout)
            self.short_wait = WebDriverWait(self.driver, WAIT_CONFIG["short_wait"])
            
            if not config.get('headless', False):
                self.driver.maximize_window()
            
        except Exception as e:
            raise Exception(f"Chrome浏览器初始化失败: {str(e)}")

    def _cleanup_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            finally:
                self.driver = None
                self.wait = None
                self.short_wait = None

    def _execute_test_steps(self, config: E2ETestConfig, test_data: Dict[str, Any], result: Dict[str, Any]):
        base_url = config.get_base_url()
        username = config.get('test_username')
        password = config.get('test_password')
        
        self._add_step_result(result, "访问网站", "执行中")
        self._navigate_to_website(base_url)
        self._add_step_result(result, "访问网站", "成功")
        
        self._add_step_result(result, "用户登录", "执行中")
        self._perform_login(username, password)
        self._add_step_result(result, "用户登录", "成功")
        
        self._add_step_result(result, "点击第一个地块卡片", "执行中")
        self._click_first_plot_card()
        self._add_step_result(result, "点击第一个地块卡片", "成功")
        
        self._add_step_result(result, "点击更多选项按钮", "执行中")
        self._click_more_options_button()
        self._add_step_result(result, "点击更多选项按钮", "成功")
        
        self._add_step_result(result, "选择疾病检测", "执行中")
        self._select_disease_detection_option()
        self._add_step_result(result, "选择疾病检测", "成功")
        
        self._add_step_result(result, "上传图片", "执行中")
        self._upload_test_image(test_data)
        self._add_step_result(result, "上传图片", "成功")
        
        self._add_step_result(result, "提交检测", "执行中")
        self._submit_detection_request()
        self._add_step_result(result, "提交检测", "成功")
        
        self._add_step_result(result, "等待结果", "执行中")
        self._wait_for_detection_result()
        self._add_step_result(result, "等待结果", "成功")
    
    def _navigate_to_website(self, base_url: str):
        try:
            print(f"[调试] 正在访问网站: {base_url}")
            self.driver.get(base_url)
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            self._wait_for_ionic_ready()
            print(f"[调试] 网站访问成功")
        except Exception as e:
            print(f"[调试] 网站访问失败: {str(e)}")
            raise Exception(f"访问网站失败: {str(e)}")
    
    def _wait_for_ionic_ready(self):
        try:
            self.short_wait.until(
                EC.any_of(*[
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    for selector in SELECTORS["ionic_ready"]
                ])
            )
            # 简化的ionic ready检查
            self.driver.execute_script("""
                if (window.Ionic && window.Ionic.isReady) {
                    console.log('Ionic is ready');
                }
            """)
            time.sleep(1)
        except Exception:
            pass
    
    def _add_step_result(self, result: Dict[str, Any], step_name: str, status: str):
        step_info = {
            "step_name": step_name,
            "status": status,
            "timestamp": time.strftime('%H:%M:%S')
        }
        result["steps"].append(step_info)
        
        if status == "执行中":
            print(f"[测试] 正在执行: {step_name}")
        elif status == "成功":
            print(f"[测试] 完成: {step_name}")
        elif status == "失败":
            print(f"[测试] 失败: {step_name}")

    def _perform_login(self, username: str, password: str):
        try:
            print(f"[调试] 开始登录流程 - 用户名: {username}")
            time.sleep(WAIT_CONFIG["navigation_delay"])
            self._wait_for_login_form()
            
            login_elements = self._find_login_elements_js()
            
            if login_elements['username'] and login_elements['password'] and login_elements['loginButton']:
                print(f"[调试] 使用JavaScript方式登录")
                self._perform_login_js(login_elements, username, password)
            else:
                print(f"[调试] 使用Selenium方式登录")
                self._perform_login_selenium(username, password)
            
            time.sleep(WAIT_CONFIG["login_delay"])
            print(f"[调试] 验证登录结果")
            self._verify_login_success()
            print(f"[调试] 登录成功")
            
        except Exception as e:
            print(f"[调试] 登录失败: {str(e)}")
            error_message = self._get_error_message()
            if error_message:
                raise Exception(f"登录失败: {error_message}")
            else:
                raise Exception(f"登录过程失败: {str(e)}")

    def _wait_for_login_form(self):
        try:
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-input[label='用户名']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
                )
            )
            time.sleep(1)
        except TimeoutException:
            raise Exception("登录表单加载超时")

    def _find_login_elements_js(self) -> Dict[str, Any]:
        try:
            return self.driver.execute_script("""
                // 查找登录元素
                const usernameInput = document.querySelector('ion-input[label="用户名"] input') || 
                                    document.querySelector('input[type="text"]');
                const passwordInput = document.querySelector('ion-input[label="密码"] input') || 
                                    document.querySelector('input[type="password"]');
                
                const loginButtons = Array.from(document.querySelectorAll('ion-button'));
                const loginButton = loginButtons.find(btn => 
                    btn.textContent.trim() === '登录' && 
                    btn.getAttribute('fill') !== 'outline'
                );
                
                return {
                    username: usernameInput,
                    password: passwordInput,
                    loginButton: loginButton
                };
            """)
        except Exception:
            return {'username': None, 'password': None, 'loginButton': None}

    def _perform_login_js(self, elements: Dict[str, Any], username: str, password: str):
        try:
            # 简化的Vue输入触发
            self.driver.execute_script("""
                const element = arguments[0];
                const value = arguments[1];
                
                if (element) {
                    element.value = value;
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """, elements['username'], username)
            time.sleep(WAIT_CONFIG["input_delay"])
            
            self.driver.execute_script("""
                const element = arguments[0];
                const value = arguments[1];
                
                if (element) {
                    element.value = value;
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """, elements['password'], password)
            time.sleep(WAIT_CONFIG["input_delay"])
            
            # 简化的Vue按钮点击
            self.driver.execute_script("""
                const button = arguments[0];
                if (button) {
                    button.click();
                }
            """, elements['loginButton'])
        except Exception as e:
            raise Exception(f"JavaScript登录执行失败: {str(e)}")

    def _perform_login_selenium(self, username: str, password: str):
        try:
            username_input = self._find_element_by_multiple_selectors(SELECTORS["login"]["username"], "用户名输入框")
            self._safe_input_vue(username_input, username, "用户名")
            
            password_input = self._find_element_by_multiple_selectors(SELECTORS["login"]["password"], "密码输入框")
            self._safe_input_vue(password_input, password, "密码")
            
            login_button = self._find_login_button()
            self._safe_click_vue(login_button, "登录按钮")
        except Exception as e:
            raise Exception(f"Selenium登录执行失败: {str(e)}")

    def _find_login_button(self):
        try:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "ion-button")
            for button in buttons:
                if button.is_displayed() and button.text.strip() == "登录":
                    fill_attr = button.get_attribute('fill')
                    if not fill_attr or fill_attr != 'outline':
                        return button
        except Exception:
            pass
        
        for selector in SELECTORS["login"]["login_button"]:
            try:
                if "contains" in selector:
                    continue
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    return element
            except NoSuchElementException:
                continue
        
        raise Exception("未找到登录按钮")

    def _safe_input_vue(self, element, text: str, field_name: str):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(WAIT_CONFIG["scroll_delay"])
            
            element.click()
            time.sleep(WAIT_CONFIG["input_delay"])
            
            element.clear()
            element.send_keys(text)
            
            if element.get_attribute('value') != text:
                # 简化的Vue输入触发
                self.driver.execute_script("""
                    const element = arguments[0];
                    const value = arguments[1];
                    
                    element.value = value;
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                """, element, text)
                time.sleep(WAIT_CONFIG["input_delay"])
        except Exception as e:
            raise Exception(f"{field_name}输入失败: {str(e)}")

    def _safe_click_vue(self, element, element_name: str):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(WAIT_CONFIG["scroll_delay"])
            
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(element))
            
            try:
                element.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", element)
                
            time.sleep(WAIT_CONFIG["click_delay"])
        except Exception as e:
            raise Exception(f"{element_name}点击失败: {str(e)}")

    def _verify_login_success(self):
        try:
            start_time = time.time()
            timeout = WAIT_CONFIG["implicit_wait"]
            
            while time.time() - start_time < timeout:
                current_url = self.driver.current_url
                
                if any(pattern in current_url for pattern in URL_VALIDATION["login_success_patterns"]):
                    if self._wait_for_home_page_loaded():
                        return
                
                if any(pattern in current_url for pattern in URL_VALIDATION["login_page_patterns"]):
                    error_msg = self._get_error_message()
                    if error_msg:
                        raise Exception(f"登录失败，错误信息: {error_msg}")
                
                time.sleep(1)
            
            current_url = self.driver.current_url
            if any(pattern in current_url for pattern in URL_VALIDATION["login_success_patterns"]):
                return
            
            if self._check_login_success_indicators():
                return
            
            raise Exception(f"登录后未跳转到预期页面，当前URL: {current_url}")
        except TimeoutException:
            raise Exception("登录验证超时")

    def _wait_for_home_page_loaded(self) -> bool:
        try:
            self.wait.until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-searchbar")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-fab ion-fab-button")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-grid")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-card"))
                )
            )
            # 简化的首页检查
            return self.driver.execute_script("""
                return document.querySelector('ion-searchbar') !== null ||
                       document.querySelector('ion-fab') !== null ||
                       document.querySelector('ion-grid') !== null;
            """)
        except TimeoutException:
            return False

    def _check_login_success_indicators(self) -> bool:
        try:
            for selector in ["ion-searchbar", "ion-fab", "ion-grid"]:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        return True
                except NoSuchElementException:
                    continue
            
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            return any(keyword in page_text for keyword in ["搜索地块", "暂无地块", "天气"])
        except Exception:
            return False

    def _click_first_plot_card(self):
        try:
            print(f"[调试] 正在查找并点击第一个地块卡片")
            time.sleep(WAIT_CONFIG["navigation_delay"])
            
            # 直接使用JavaScript查找第一个地块卡片
            first_plot_card = self.driver.execute_script("""
                // 查找第一个地块卡片
                const plotCards = Array.from(document.querySelectorAll('ion-card[router-link*="/tabs/strip/"]'));
                if (plotCards.length > 0) {
                    return plotCards[0];
                }
                
                // 备用方案：查找网格中的第一个卡片
                const gridCards = Array.from(document.querySelectorAll('ion-grid ion-row ion-col ion-card[button]'));
                if (gridCards.length > 0) {
                    return gridCards[0];
                }
                
                return null;
            """)
            
            if first_plot_card:
                print(f"[调试] 通过JavaScript找到第一个地块卡片")
                self._safe_click_vue(first_plot_card, "第一个地块卡片")
            else:
                print(f"[调试] JavaScript未找到地块卡片，使用Selenium方式查找")
                plot_cards = self._find_plot_cards()
                if not plot_cards:
                    print(f"[调试] 未找到任何地块卡片")
                    raise Exception("未找到任何地块卡片")
                print(f"[调试] 找到 {len(plot_cards)} 个地块卡片")
                self._safe_click_vue(plot_cards[0], "第一个地块卡片")
            
            time.sleep(WAIT_CONFIG["plot_detail_delay"])
            
            current_url = self.driver.current_url
            print(f"[调试] 当前URL: {current_url}")
            if not any(pattern in current_url for pattern in URL_VALIDATION["plot_detail_patterns"]):
                raise Exception(f"未成功跳转到地块详情页")
            print(f"[调试] 成功跳转到地块详情页")
        except Exception as e:
            print(f"[调试] 点击地块卡片失败: {str(e)}")
            raise Exception(f"点击第一个地块卡片失败: {str(e)}")

    def _click_more_options_button(self):
        try:
            print(f"[调试] 正在点击更多选项按钮")
            time.sleep(WAIT_CONFIG["navigation_delay"])
            
            # 首先尝试 JavaScript 点击
            click_result = self.driver.execute_script("""
                var button = document.querySelector('#more-options-button');
                if (button) {
                    console.log('[JS] 找到更多选项按钮，准备点击');
                    button.click();
                    return { success: true };
                }
                return { success: false, error: '未找到按钮' };
            """)
            
            if click_result.get('success'):
                print(f"[调试] JavaScript 点击成功")
            else:
                print(f"[调试] JavaScript 点击失败，使用 Selenium 方式")
                more_button = self._find_element_by_multiple_selectors(
                    SELECTORS["plot_detail"]["more_options_button"], "更多选项按钮"
                )
                self._safe_click_vue(more_button, "更多选项按钮")
            
            # 等待 Popover 出现
            time.sleep(WAIT_CONFIG["click_delay"] * 2)  # 稍微多等一会
            
            # 验证 Popover 是否出现
            popover_visible = self.driver.execute_script("""
                var popover = document.querySelector('ion-popover');
                return popover && popover.offsetParent !== null;
            """)
            
            if popover_visible:
                print(f"[调试] Popover 已显示")
            else:
                print(f"[调试] Popover 未显示，可能需要再次点击")
                # 如果 Popover 没有显示，再尝试一次点击
                time.sleep(1)
                self.driver.execute_script("""
                    var button = document.querySelector('#more-options-button');
                    if (button) {
                        button.click();
                    }
                """)
                time.sleep(WAIT_CONFIG["click_delay"])
            
            print(f"[调试] 更多选项按钮点击完成")
            
        except Exception as e:
            print(f"[调试] 点击更多选项按钮失败: {str(e)}")
            raise Exception(f"点击更多选项按钮失败: {str(e)}")

    def _select_disease_detection_option(self):
        try:
            print(f"[调试] 正在查找疾病检测选项")
            time.sleep(WAIT_CONFIG["click_delay"])
            
            # 等待 Popover 出现和渲染完成
            print(f"[调试] 等待 Popover 显示...")
            try:
                # 等待 Popover 容器出现
                self.short_wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-popover"))
                )
                print(f"[调试] Popover 容器已出现")
                
                # 再等待一段时间确保内容渲染完成
                time.sleep(WAIT_CONFIG["navigation_delay"])
                
                # 等待 Popover 内容加载
                self.short_wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "ion-popover ion-content"))
                )
                print(f"[调试] Popover 内容已加载")
                
            except TimeoutException:
                print(f"[调试] Popover 未能及时显示，尝试继续...")
        
            # 使用 JavaScript 直接查找和点击疾病检测选项
            detection_clicked = self.driver.execute_script("""
                console.log('[JS] 开始查找疾病检测选项');
                
                // 查找 Popover 中的所有 ion-item
                var popover = document.querySelector('ion-popover');
                if (!popover) {
                    console.log('[JS] 未找到 ion-popover');
                    return { success: false, error: '未找到 Popover' };
                }
                
                var items = popover.querySelectorAll('ion-item');
                console.log('[JS] 在 Popover 中找到', items.length, '个 ion-item');
                
                for (var i = 0; i < items.length; i++) {
                    var item = items[i];
                    var text = item.textContent.trim();
                    console.log('[JS] 项目', i, '文本:', text);
                    
                    if (text.includes('疾病检测')) {
                        console.log('[JS] 找到疾病检测选项，准备点击');
                        
                        // 触发 Vue 的点击事件
                        item.dispatchEvent(new Event('click', { bubbles: true }));
                        
                        // 也尝试直接点击
                        item.click();
                        
                        return { success: true, text: text };
                    }
                }
                
                return { success: false, error: '未找到疾病检测选项', itemCount: items.length };
            """)
            
            if detection_clicked and detection_clicked.get('success'):
                print(f"[调试] JavaScript 成功点击疾病检测选项: {detection_clicked.get('text')}")
            else:
                print(f"[调试] JavaScript 未能点击疾病检测选项: {detection_clicked.get('error')}")
                print(f"[调试] 尝试使用 Selenium 方式查找...")
                
                # 备用方案：使用 Selenium 查找
                self._find_and_click_disease_detection_selenium()
            
            # 等待疾病检测模态框出现 - 增加等待时间和更灵活的检查
            print(f"[调试] 等待疾病检测模态框出现...")
            
            # 等待Vue组件状态更新
            time.sleep(WAIT_CONFIG["navigation_delay"] * 2)  # 增加等待时间
            
            # 使用更灵活的方式检查模态框
            modal_opened = False
            max_attempts = 10
            
            for attempt in range(max_attempts):
                print(f"[调试] 检查模态框状态 (尝试 {attempt + 1}/{max_attempts})")
                
                modal_status = self.driver.execute_script("""
                    // 检查所有可能的模态框状态
                    var modals = document.querySelectorAll('ion-modal');
                    var modalInfo = [];
                    
                    for (var i = 0; i < modals.length; i++) {
                        var modal = modals[i];
                        var info = {
                            index: i,
                            isOpen: modal.getAttribute('is-open'),
                            visible: modal.offsetParent !== null,
                            display: window.getComputedStyle(modal).display,
                            contains: modal.textContent.includes('疾病检测') || modal.textContent.includes('检测')
                        };
                        modalInfo.push(info);
                        
                        // 如果找到疾病检测模态框且已打开
                        if (info.contains && (info.isOpen === 'true' || info.visible)) {
                            return { success: true, modalIndex: i, info: info };
                        }
                    }
                    
                    return { success: false, modals: modalInfo };
                """)
                
                if modal_status.get('success'):
                    print(f"[调试] 找到已打开的疾病检测模态框: {modal_status.get('info')}")
                    modal_opened = True
                    break
                else:
                    print(f"[调试] 模态框状态: {modal_status.get('modals')}")
                    time.sleep(1)  # 等待1秒后再次检查
            
            if not modal_opened:
                print(f"[调试] 模态框未能打开，尝试使用传统方式检查...")
                
                # 传统方式检查模态框
                try:
                    # 尝试查找任何包含疾病检测内容的模态框
                    modal_elements = self.driver.find_elements(By.CSS_SELECTOR, "ion-modal")
                    print(f"[调试] 找到 {len(modal_elements)} 个模态框元素")
                    
                    for i, modal in enumerate(modal_elements):
                        try:
                            if modal.is_displayed():
                                modal_text = modal.text
                                print(f"[调试] 模态框 {i+1} 内容预览: {modal_text[:100]}...")
                                if "疾病检测" in modal_text or "检测" in modal_text:
                                    print(f"[调试] 找到疾病检测模态框 (传统方式)")
                                    modal_opened = True
                                    break
                        except Exception as e:
                            print(f"[调试] 检查模态框 {i+1} 时出错: {str(e)}")
                            continue
                    
                    if not modal_opened:
                        # 最后尝试：等待任何模态框打开
                        try:
                            self.short_wait.until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "ion-modal[is-open='true']"))
                            )
                            print(f"[调试] 检测到有模态框已打开")
                            modal_opened = True
                        except TimeoutException:
                            pass
                        
                except Exception as e:
                    print(f"[调试] 传统方式检查模态框失败: {str(e)}")
            
            if not modal_opened:
                print(f"[调试] 疾病检测模态框仍未打开，检查页面状态...")
                self._debug_page_state()
                
                # 尝试再次点击疾病检测选项
                print(f"[调试] 尝试再次点击疾病检测选项...")
                time.sleep(2)
                
                retry_clicked = self.driver.execute_script("""
                    // 再次尝试找到并点击疾病检测选项
                    var items = document.querySelectorAll('ion-item');
                    for (var i = 0; i < items.length; i++) {
                        var item = items[i];
                        if (item.textContent.includes('疾病检测') && item.offsetParent !== null) {
                            console.log('[JS] 重新点击疾病检测选项');
                            item.click();
                            return true;
                        }
                    }
                    return false;
                """)
                
                if retry_clicked:
                    print(f"[调试] 重新点击成功，再次等待模态框...")
                    time.sleep(3)
                    
                    # 再次检查模态框
                    final_check = self.driver.execute_script("""
                        var modals = document.querySelectorAll('ion-modal');
                        for (var i = 0; i < modals.length; i++) {
                            var modal = modals[i];
                            if ((modal.getAttribute('is-open') === 'true' || modal.offsetParent !== null) && 
                                modal.textContent.includes('疾病检测')) {
                                return true;
                            }
                        }
                        return false;
                    """)
                    
                    if final_check:
                        print(f"[调试] 重新点击后模态框已打开")
                        modal_opened = True
            
            if not modal_opened:
                raise Exception("疾病检测模态框未打开")
            else:
                print(f"[调试] 疾病检测模态框已成功打开")
                
        except Exception as e:
            print(f"[调试] 选择疾病检测选项失败: {str(e)}")
            raise Exception(f"选择疾病检测选项失败: {str(e)}")

    def _find_and_click_disease_detection_selenium(self):
        """使用 Selenium 方式查找并点击疾病检测选项"""
        try:
            # 查找 Popover 容器
            popover = self.driver.find_element(By.CSS_SELECTOR, "ion-popover")
            if not popover:
                raise Exception("未找到 Popover 容器")
            
            # 在 Popover 中查找所有 ion-item
            menu_items = popover.find_elements(By.CSS_SELECTOR, "ion-item")
            print(f"[调试] Selenium 在 Popover 中找到 {len(menu_items)} 个菜单项")
            
            detection_item = None
            for i, item in enumerate(menu_items):
                if item.is_displayed():
                    item_text = item.text.strip()
                    print(f"[调试] 菜单项 {i+1}: {item_text}")
                    if "疾病检测" in item_text:
                        detection_item = item
                        print(f"[调试] 找到疾病检测选项")
                        break
            
            if not detection_item:
                # 如果还是找不到，尝试更宽泛的查找
                all_items = self.driver.find_elements(By.CSS_SELECTOR, "ion-item")
                print(f"[调试] 在整个页面找到 {len(all_items)} 个 ion-item")
                for i, item in enumerate(all_items):
                    if item.is_displayed():
                        item_text = item.text.strip()
                        print(f"[调试] 页面菜单项 {i+1}: {item_text}")
                        if "疾病检测" in item_text:
                            detection_item = item
                            print(f"[调试] 在页面中找到疾病检测选项")
                            break
            
            if not detection_item:
                raise Exception("未找到疾病检测选项")
            
            self._safe_click_vue(detection_item, "疾病检测选项")
            
        except Exception as e:
            print(f"[调试] Selenium 查找疾病检测选项失败: {str(e)}")
            raise

    def _debug_page_state(self):
        """调试页面状态 - 增强版"""
        try:
            page_info = self.driver.execute_script("""
                var modals = document.querySelectorAll('ion-modal');
                var modalDetails = [];
                
                for (var i = 0; i < modals.length; i++) {
                    var modal = modals[i];
                    modalDetails.push({
                        index: i,
                        isOpen: modal.getAttribute('is-open'),
                        visible: modal.offsetParent !== null,
                        display: window.getComputedStyle(modal).display,
                        textContent: modal.textContent.substring(0, 100),
                        className: modal.className,
                        hasDetectionText: modal.textContent.includes('疾病检测') || modal.textContent.includes('检测')
                    });
                }
                
                return {
                    url: window.location.href,
                    title: document.title,
                    popoverCount: document.querySelectorAll('ion-popover').length,
                    modalCount: document.querySelectorAll('ion-modal').length,
                    itemCount: document.querySelectorAll('ion-item').length,
                    visibleItemCount: Array.from(document.querySelectorAll('ion-item')).filter(el => el.offsetParent !== null).length,
                    popoverVisible: Array.from(document.querySelectorAll('ion-popover')).some(el => el.offsetParent !== null),
                    modalOpen: Array.from(document.querySelectorAll('ion-modal')).some(el => el.getAttribute('is-open') === 'true'),
                    modalDetails: modalDetails
                };
            """)
            print(f"[调试] 详细页面状态: {page_info}")
        except Exception as e:
            print(f"[调试] 获取页面状态失败: {str(e)}")

    def _upload_test_image(self, test_data: Dict[str, Any]):
        try:
            image_path = test_data.get('image_path', os.path.join(self.test_data_dir, DEFAULT_TEST_IMAGE["filename"]))
            print(f"[调试] 准备上传图片: {image_path}")
            
            if not os.path.exists(image_path):
                print(f"[调试] 测试图片不存在: {image_path}")
                raise Exception(f"测试图片不存在: {image_path}")
            
            print(f"[调试] 图片文件存在，大小: {os.path.getsize(image_path)} 字节")
            time.sleep(WAIT_CONFIG["navigation_delay"])
            
            file_input = self._find_element_by_multiple_selectors(
                SELECTORS["disease_detection"]["file_input"], "文件上传输入框"
            )
            print(f"[调试] 找到文件上传输入框")
            
            absolute_path = os.path.abspath(image_path)
            file_input.send_keys(absolute_path)
            print(f"[调试] 文件路径已发送到输入框")
            time.sleep(WAIT_CONFIG["input_delay"])
            
            file_value = file_input.get_attribute('value')
            if not file_value:
                print(f"[调试] 文件上传失败，输入框值为空")
                raise Exception("文件上传失败")
            else:
                print(f"[调试] 文件上传成功，输入框值: {file_value}")
        except Exception as e:
            print(f"[调试] 上传图片失败: {str(e)}")
            raise Exception(f"上传测试图片失败: {str(e)}")

    def _submit_detection_request(self):
        try:
            print(f"[调试] 正在查找并点击提交检测按钮")
            submit_button = self._find_element_by_multiple_selectors(
                SELECTORS["disease_detection"]["submit_button"], "提交检测按钮"
            )
            print(f"[调试] 找到提交检测按钮")
            
            if submit_button.get_attribute('disabled'):
                print(f"[调试] 提交按钮被禁用")
                raise Exception("提交按钮被禁用")
            
            print(f"[调试] 提交按钮可用，正在点击")
            self._safe_click_vue(submit_button, "提交检测按钮")
            print(f"[调试] 提交检测按钮点击完成")
        except Exception as e:
            print(f"[调试] 提交检测失败: {str(e)}")
            raise Exception(f"提交检测请求失败: {str(e)}")

    def _wait_for_detection_result(self):
        """等待检测结果 - 优化版"""
        try:
            max_wait_time = DETECTION_WAIT_CONFIG["max_wait_time"]
            check_interval = DETECTION_WAIT_CONFIG["check_interval"]
            print(f"[调试] 开始等待检测结果，最大等待时间: {max_wait_time}秒")
            
            # 先等待一段时间让请求处理
            print(f"[调试] 等待检测请求处理...")
            time.sleep(3)
            
            for attempt in range(max_wait_time // check_interval):
                elapsed_time = (attempt + 1) * check_interval
                print(f"[调试] 等待检测结果中... ({elapsed_time}/{max_wait_time}秒)")
                
                # 检查是否有错误信息
                error_msg = self._check_for_error_message()
                if error_msg:
                    print(f"[调试] 检测过程中出现错误: {error_msg}")
                    raise Exception(f"检测过程中出现错误: {error_msg}")
                
                # 检查检测结果
                if self._check_for_detection_result():
                    print(f"[调试] 检测结果已出现，等待时间: {elapsed_time}秒")
                    # 额外等待一下确保结果完整加载
                    time.sleep(2)
                    return True
                
                # 检查是否有成功提示
                success_alert = self._check_for_success_alert()
                if success_alert:
                    print(f"[调试] 检测到成功提示，继续等待结果显示...")
                    time.sleep(3)
                    continue
                
                time.sleep(check_interval)
            
            # 超时后最后检查一次
            print(f"[调试] 等待超时，进行最终检查...")
            if self._check_final_result():
                print(f"[调试] 最终检查发现结果")
                return True
            
            print(f"[调试] 检测处理超时，未找到有效结果")
            raise Exception(f"检测处理超时")
            
        except Exception as e:
            print(f"[调试] 等待检测结果失败: {str(e)}")
            raise Exception(f"等待检测结果失败: {str(e)}")

    def _check_for_success_alert(self) -> bool:
        """检查是否有成功提示"""
        try:
            return self.driver.execute_script("""
                // 检查 ion-alert
                var alerts = document.querySelectorAll('ion-alert');
                for (var i = 0; i < alerts.length; i++) {
                    var alert = alerts[i];
                    if (alert.offsetParent !== null) {  // 可见的alert
                        var text = alert.textContent.toLowerCase();
                        if (text.includes('成功') || text.includes('检测完成') || text.includes('success')) {
                            return true;
                        }
                    }
                }
                
                // 检查 ion-toast
                var toasts = document.querySelectorAll('ion-toast');
                for (var i = 0; i < toasts.length; i++) {
                    var toast = toasts[i];
                    if (toast.offsetParent !== null) {
                        var text = toast.textContent.toLowerCase();
                        if (text.includes('成功') || text.includes('检测完成') || text.includes('success')) {
                            return true;
                        }
                    }
                }
                
                return false;
            """)
        except Exception:
            return False

    def _check_final_result(self) -> bool:
        """最终检查结果"""
        try:
            print(f"[调试] 执行最终结果检查...")
            
            # 1. 检查页面是否有任何结果内容
            page_info = self.driver.execute_script("""
                var pageText = document.body.textContent.toLowerCase();
                var hasResultKeywords = pageText.includes('病害名称') || 
                                      pageText.includes('检测结果') || 
                                      pageText.includes('置信度') || 
                                      pageText.includes('建议');
                
                var modalCount = document.querySelectorAll('ion-modal[is-open="true"]').length;
                var cardCount = document.querySelectorAll('ion-card').length;
                var logCount = document.querySelectorAll('ion-list ion-item').length;
                
                return {
                    hasResultKeywords: hasResultKeywords,
                    modalCount: modalCount,
                    cardCount: cardCount,
                    logCount: logCount,
                    currentUrl: window.location.href
                };
            """)
            
            print(f"[调试] 最终检查结果: {page_info}")
            
            if page_info and page_info.get('hasResultKeywords'):
                print(f"[调试] 页面包含结果关键词")
                return True
            
            # 2. 检查传统方式
            return self._has_any_result_content()
            
        except Exception as e:
            print(f"[调试] 最终检查失败: {str(e)}")
            return False

    def _has_any_result_content(self) -> bool:
        """检查是否有任何结果内容 - 增强版"""
        try:
            page_source = self.driver.page_source.lower()
            
            # 更具体的关键词检查
            result_keywords = [
                "检测结果", "病害名称", "置信度", "建议", 
                "detection", "result", "disease", "confidence"
            ]
            
            success_keywords = [
                "检测完成", "分析完成", "处理完成", "成功",
                "detection complete", "analysis complete", "success"
            ]
            
            found_result_keywords = [k for k in result_keywords if k in page_source]
            found_success_keywords = [k for k in success_keywords if k in page_source]
            
            print(f"[调试] 找到结果关键词: {found_result_keywords}")
            print(f"[调试] 找到成功关键词: {found_success_keywords}")
            
            # 如果找到足够的关键词，认为有结果
            if len(found_result_keywords) >= 2 or len(found_success_keywords) >= 1:
                return True
            
            # 检查是否有新的日志项目（检测完成后会刷新数据）
            try:
                log_items = self.driver.find_elements(By.CSS_SELECTOR, "ion-list ion-item")
                if len(log_items) > 0:
                    latest_log = log_items[0]
                    log_text = latest_log.text.lower()
                    if any(keyword in log_text for keyword in ["检测", "病害", "识别", "分析"]):
                        print(f"[调试] 发现新的检测相关日志")
                        return True
            except Exception as e:
                print(f"[调试] 检查日志项目失败: {str(e)}")
            
            return False
            
        except Exception:
            return False

    def _find_plot_cards(self):
        try:
            # 使用JavaScript查找
            plot_cards = self.driver.execute_script("""
                return Array.from(document.querySelectorAll('ion-card[router-link*="/tabs/strip/"]'));
            """)
            if plot_cards:
                return plot_cards
        except Exception:
            pass
        
        for selector in SELECTORS["plot_cards"]:
            try:
                cards = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
                visible_cards = [card for card in cards if card.is_displayed() and card.is_enabled()]
                if visible_cards:
                    return visible_cards
            except TimeoutException:
                continue
        
        return []

    def _find_element_by_multiple_selectors(self, selectors: List[str], element_name: str):
        for selector in selectors:
            try:
                if "contains" in selector:
                    continue
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    return element
            except NoSuchElementException:
                continue
        raise Exception(f"未找到{element_name}")

    def _get_error_message(self) -> str:
        try:
            for selector in SELECTORS["error_messages"]:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if element.is_displayed():
                        return element.text.strip()
                except NoSuchElementException:
                    continue
        except Exception:
            pass
        return ""

    def _take_screenshot(self, name: str) -> str:
        try:
            timestamp = int(time.time())
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            self.driver.save_screenshot(filepath)
            print(f"[调试] 截图已保存: {filepath}")
            return filepath
        except Exception as e:
            print(f"[调试] 截图失败: {str(e)}")
            return None

    # 天气信息测试方法
    def get_weather_predefined_test_cases(self) -> List[Dict[str, Any]]:
        return [TEST_CASES_CONFIG["weather_info"]]
    
    def run_weather_info_test(self, test_config: Dict[str, Any]) -> Dict[str, Any]:
        print(f"\n[测试开始] 天气信息测试")
        print(f"[配置] 基础URL: {test_config.get('base_url', '未设置')}")
        
        test_result = {
            "test_id": TEST_CASES_CONFIG["weather_info"]["test_id"],
            "test_name": TEST_CASES_CONFIG["weather_info"]["test_name"],
            "start_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "status": "RUNNING",
            "steps": [],
            "weather_data": {},
            "error_message": None,
            "execution_time": 0
        }
        
        start_time = time.time()
        
        try:
            print(f"[调试] 设置浏览器驱动")
            self._setup_driver(test_config)
            print(f"[调试] 开始执行天气测试步骤")
            self._execute_weather_test_steps(test_config, test_result)
            test_result["status"] = "PASSED"
            test_result["message"] = "天气信息测试执行成功"
            print(f"\n[测试成功] 天气信息测试执行成功")
        except Exception as e:
            test_result["status"] = "FAILED"
            test_result["error_message"] = str(e)
            test_result["message"] = f"天气信息测试执行失败: {str(e)}"
            print(f"\n[测试失败] {str(e)}")
        finally:
            print(f"[调试] 清理浏览器驱动")
            self._cleanup_driver()
            test_result["execution_time"] = round(time.time() - start_time, 2)
            test_result["end_time"] = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[调试] 执行时间: {test_result['execution_time']}秒")
            
        print(f"\n[测试结束] 天气信息测试")
        return test_result
    
    def _execute_weather_test_steps(self, config: Dict[str, Any], result: Dict[str, Any]):
        config_obj = E2ETestConfig(config)
        base_url = config_obj.get_base_url()
        username = config_obj.get('test_username')
        password = config_obj.get('test_password')
        
        self._add_step_result(result, "访问网站", "执行中")
        self._navigate_to_website(base_url)
        self._add_step_result(result, "访问网站", "成功")
        
        self._add_step_result(result, "用户登录", "执行中")
        self._perform_login(username, password)
        self._add_step_result(result, "用户登录", "成功")
        
        self._add_step_result(result, "验证天气信息", "执行中")
        weather_data = self._verify_weather_info_display()
        result["weather_data"] = weather_data
        self._add_step_result(result, "验证天气信息", "成功")
    
    def _verify_weather_info_display(self) -> Dict[str, Any]:
        print(f"[调试] 开始验证天气信息显示")
        time.sleep(WAIT_CONFIG["weather_info_delay"])
        
        try:
            # 简化的天气卡片查找
            weather_container = self.driver.execute_script("""
                return Array.from(document.querySelectorAll('ion-card')).find(card => {
                    const title = card.querySelector('ion-card-title');
                    return title && title.textContent.includes('天气');
                });
            """)
            
            if not weather_container:
                print(f"[调试] JavaScript未找到天气容器，使用Selenium方式查找")
                for i, selector in enumerate(SELECTORS["weather_info"]):
                    try:
                        container = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if container.is_displayed():
                            print(f"[调试] 通过选择器 {i+1} 找到天气容器")
                            weather_container = container
                            break
                    except NoSuchElementException:
                        print(f"[调试] 选择器 {i+1} 未找到天气容器")
                        continue
            else:
                print(f"[调试] JavaScript找到天气容器")
            
            if not weather_container:
                print(f"[调试] 未找到天气信息容器")
                raise Exception("未找到天气信息容器")
            
            print(f"[调试] 开始提取天气数据")
            weather_data = self._extract_weather_data(weather_container)
            print(f"[调试] 提取到的天气数据: {weather_data}")
            
            if not any(weather_data.values()):
                print(f"[调试] 天气信息容器存在但未找到具体天气数据")
                raise Exception("天气信息容器存在但未找到具体天气数据")
            
            weather_data["status"] = "天气信息获取成功"
            print(f"[调试] 天气信息验证成功")
            return weather_data
        except Exception as e:
            print(f"[调试] 天气信息验证失败: {str(e)}")
            raise Exception(f"天气信息验证失败: {str(e)}")

    def _extract_weather_data(self, container) -> Dict[str, Any]:
        weather_data = {}
        
        try:
            title_element = container.find_element(By.CSS_SELECTOR, "ion-card-title")
            if title_element and title_element.is_displayed():
                weather_data["title"] = title_element.text.strip()
            
            paragraphs = container.find_elements(By.CSS_SELECTOR, "ion-card-content p")
            for i, p in enumerate(paragraphs):
                if p.is_displayed():
                    text = p.text.strip()
                    if text:
                        if "°C" in text:
                            weather_data["temperature"] = text
                        elif "天气" in text:
                            weather_data[f"weather_{i}"] = text
                        else:
                            weather_data[f"info_{i}"] = text
            
            if not weather_data:
                weather_data["container_text"] = container.text.strip()
        except Exception as e:
            weather_data["error"] = str(e)
        
        return weather_data
    def _check_for_error_message(self) -> str:
        """检查是否有错误信息"""
        try:
            # 检查各种可能的错误提示
            error_msg = self.driver.execute_script("""
                // 检查 ion-alert 中的错误信息
                var alerts = document.querySelectorAll('ion-alert');
                for (var i = 0; i < alerts.length; i++) {
                    var alert = alerts[i];
                    if (alert.offsetParent !== null) {
                        var text = alert.textContent.toLowerCase();
                        if (text.includes('错误') || text.includes('失败') || text.includes('error') || text.includes('failed')) {
                            return alert.textContent.trim();
                        }
                    }
                }
                
                // 检查 ion-toast 中的错误信息
                var toasts = document.querySelectorAll('ion-toast');
                for (var i = 0; i < toasts.length; i++) {
                    var toast = toasts[i];
                    if (toast.offsetParent !== null) {
                        var text = toast.textContent.toLowerCase();
                        if (text.includes('错误') || text.includes('失败') || text.includes('error') || text.includes('failed')) {
                            return toast.textContent.trim();
                        }
                    }
                }
                
                // 检查模态框中的错误信息
                var modals = document.querySelectorAll('ion-modal[is-open="true"]');
                for (var i = 0; i < modals.length; i++) {
                    var modal = modals[i];
                    var text = modal.textContent.toLowerCase();
                    if (text.includes('错误') || text.includes('失败') || text.includes('error') || text.includes('failed')) {
                        // 获取具体的错误信息
                        var errorElements = modal.querySelectorAll('p, span, div');
                        for (var j = 0; j < errorElements.length; j++) {
                            var elem = errorElements[j];
                            var elemText = elem.textContent.toLowerCase();
                            if (elemText.includes('错误') || elemText.includes('失败')) {
                                return elem.textContent.trim();
                            }
                        }
                    }
                }
                
                return '';
            """)
            
            if error_msg:
                print(f"[调试] 检测到错误信息: {error_msg}")
                return error_msg
            
            # 备用方案：使用Selenium查找错误信息
            try:
                for selector in SELECTORS["error_messages"]:
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if element.is_displayed():
                            error_text = element.text.strip()
                            if error_text and any(keyword in error_text.lower() for keyword in ["错误", "失败", "error", "failed"]):
                                print(f"[调试] Selenium检测到错误信息: {error_text}")
                                return error_text
                    except NoSuchElementException:
                        continue
            except Exception as e:
                print(f"[调试] Selenium检查错误信息失败: {str(e)}")
            
            return ""
            
        except Exception as e:
            print(f"[调试] 检查错误信息失败: {str(e)}")
            return ""

    def _check_for_detection_result(self) -> bool:
        """检查检测结果是否出现"""
        print(f"[调试] 开始检查检测结果...")
        
        # 使用 JavaScript 进行更全面的检查
        result_found = self.driver.execute_script("""
            console.log('[JS] 开始检查检测结果');
            
            // 1. 检查模态框中的检测结果卡片
            var modals = document.querySelectorAll('ion-modal[is-open="true"]');
            console.log('[JS] 找到', modals.length, '个打开的模态框');
            
            for (var i = 0; i < modals.length; i++) {
                var modal = modals[i];
                
                // 检查是否包含检测结果相关内容
                var text = modal.textContent.toLowerCase();
                if (text.includes('检测结果') || text.includes('病害名称') || text.includes('置信度') || text.includes('建议')) {
                    console.log('[JS] 模态框', i, '包含检测结果内容');
                    
                    // 查找具体的结果卡片
                    var resultCard = modal.querySelector('ion-card ion-card-title');
                    if (resultCard && resultCard.textContent.includes('检测结果')) {
                        console.log('[JS] 找到检测结果卡片');
                        
                        // 检查卡片内容是否完整
                        var cardContent = modal.querySelector('ion-card ion-card-content');
                        if (cardContent) {
                            var contentText = cardContent.textContent;
                            var hasDiseaseName = contentText.includes('病害名称');
                            var hasAdvice = contentText.includes('建议');
                            var hasPercent = contentText.includes('置信度') || contentText.includes('%');
                            
                            console.log('[JS] 检测结果内容:', {
                                hasDiseaseName: hasDiseaseName,
                                hasAdvice: hasAdvice,
                                hasPercent: hasPercent,
                                contentPreview: contentText.substring(0, 100)
                            });
                            
                            if (hasDiseaseName && hasAdvice && hasPercent) {
                                console.log('[JS] 检测结果完整');
                                return { found: true, complete: true };
                            } else if (hasDiseaseName || hasAdvice || hasPercent) {
                                console.log('[JS] 检测结果部分显示');
                                return { found: true, complete: false };
                            }
                        }
                    }
                }
            }
            
            // 2. 检查是否有成功的提示信息
            var alerts = document.querySelectorAll('ion-alert');
            for (var i = 0; i < alerts.length; i++) {
                var alert = alerts[i];
                if (alert.offsetParent !== null && (alert.textContent.includes('检测完成') || alert.textContent.includes('成功'))) {
                    console.log('[JS] 找到成功提示');
                    return { found: true, complete: false, hasAlert: true };
                }
            }
            
            // 3. 检查页面是否有新的日志记录（检测完成后会刷新页面数据）
            var logItems = document.querySelectorAll('ion-list ion-item');
            console.log('[JS] 找到', logItems.length, '个日志项');
            if (logItems.length > 0) {
                // 检查最新的日志是否包含检测相关内容
                var latestLog = logItems[0];
                var logText = latestLog.textContent.toLowerCase();
                if (logText.includes('检测') || logText.includes('病害') || logText.includes('置信度')) {
                    console.log('[JS] 找到检测相关日志');
                    return { found: true, complete: true, hasLog: true };
                }
            }
            
            console.log('[JS] 未找到检测结果');
            return { found: false };
        """)
        
        if result_found and result_found.get('found'):
            is_complete = result_found.get('complete', False)
            has_alert = result_found.get('hasAlert', False)
            has_log = result_found.get('hasLog', False)
            
            print(f"[调试] 检测结果状态: 完整={is_complete}, 有提示={has_alert}, 有日志={has_log}")
            
            if is_complete:
                print(f"[调试] 检测结果完整显示")
                return True
            elif has_alert:
                print(f"[调试] 检测完成提示出现，等待结果显示...")
                time.sleep(3)  # 等待结果渲染
                # 再次检查结果是否显示
                return self._check_detection_result_again()
            elif has_log:
                print(f"[调试] 检测结果已添加到日志")
                return True
            else:
                print(f"[调试] 检测结果部分显示，继续等待...")
                return False
        else:
            print(f"[调试] 未找到检测结果")
            return False

    def _check_detection_result_again(self) -> bool:
        """再次检查检测结果"""
        print(f"[调试] 再次检查检测结果...")
        
        try:
            # 检查模态框中的结果
            modal_result = self.driver.execute_script("""
                var modals = document.querySelectorAll('ion-modal[is-open="true"]');
                for (var i = 0; i < modals.length; i++) {
                    var modal = modals[i];
                    var resultCard = modal.querySelector('ion-card ion-card-content');
                    if (resultCard) {
                        var text = resultCard.textContent;
                        if (text.includes('病害名称') && text.includes('建议') && text.includes('置信度')) {
                            return true;
                        }
                    }
                }
                return false;
            """)
            
            if modal_result:
                print(f"[调试] 模态框中检测结果已完整显示")
                return True
            
            # 检查是否有新的日志记录
            log_result = self.driver.execute_script("""
                var logItems = document.querySelectorAll('ion-list ion-item');
                if (logItems.length > 0) {
                    var latestLog = logItems[0];
                    var logText = latestLog.textContent.toLowerCase();
                    return logText.includes('检测') || logText.includes('病害');
                }
                return false;
            """)
            
            if log_result:
                print(f"[调试] 检测结果已添加到日志记录")
                return True
            
            print(f"[调试] 再次检查未找到完整结果")
            return False
            
        except Exception as e:
            print(f"[调试] 再次检查检测结果时出错: {str(e)}")
            return False


# 工具类
class E2ETestUtils:
    @staticmethod
    def validate_test_config(config: Dict[str, Any]) -> Dict[str, Any]:
        validated_config = {**DEFAULT_TEST_CONFIG, **config}
        
        required_fields = ["base_url", "test_username", "test_password"]
        for field in required_fields:
            if not validated_config.get(field):
                raise ValueError(f"缺少必要配置项: {field}")
        
        return validated_config
    
    @staticmethod
    def validate_test_data(test_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证测试数据"""
        default_data = {
            "image_path": os.path.join(TEST_DIRECTORIES["test_data"], DEFAULT_TEST_IMAGE["filename"])
        }
        
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
        """创建默认测试图片"""
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
                with open(image_path + ".txt", 'w') as f:
                    f.write("测试图片占位符 - 请手动准备测试图片")
                print(f"[调试] PIL不可用，创建测试图片占位符: {image_path}.txt")
                return False
                
        except Exception as e:
            print(f"[调试] 创建默认测试图片失败: {e}")
            return False
    
    @staticmethod
    def generate_test_report(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.get("status") == "PASSED"])
        
        return {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "pass_rate": round((passed_tests / total_tests * 100), 2) if total_tests > 0 else 0
            },
            "test_results": test_results,
            "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }