"""
系统测试配置文件
包含所有E2E测试相关的配置项
"""

# 默认测试配置
DEFAULT_TEST_CONFIG = {
    "base_url": "http://127.0.0.1:4000",
    "test_username": "cxk",
    "test_password": "cxk",
    "headless": False,
    "timeout": 30
}

# 浏览器配置
CHROME_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-web-security',
    '--disable-features=VizDisplayCompositor',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-images',
    '--memory-pressure-off',
    '--max_old_space_size=4096',
    '--disable-background-timer-throttling',
    '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows',
    '--aggressive-cache-discard',
    '--disable-background-networking',
    '--enable-logging',
    '--log-level=0',
    '--v=1'
]

# headless模式下的窗口大小
HEADLESS_WINDOW_SIZE = '--window-size=1920,1080'

# 最大化窗口选项
MAXIMIZED_WINDOW = '--start-maximized'

# 目录配置
TEST_DIRECTORIES = {
    "test_data": "test_data",
    "screenshots": "test_screenshots",
    "downloads": "downloads"
}

# 默认测试图片配置
DEFAULT_TEST_IMAGE = {
    "filename": "disease_sample.jpg",
    "size": (300, 200),
    "color": "green"
}

# 测试重试配置
RETRY_CONFIG = {
    "max_retries": 3,
    "retry_delay": 5,  # 秒
    "browser_error_keywords": ["chrome", "webdriver", "connection"]
}

# 等待时间配置
WAIT_CONFIG = {
    "implicit_wait": 30,
    "page_load_timeout": 30,
    "script_timeout": 30,
    "short_wait": 5,
    "ionic_ready_timeout": 10,
    "navigation_delay": 2,
    "login_delay": 2,
    "plot_detail_delay": 3,
    "weather_info_delay": 3,
    "input_delay": 1,
    "click_delay": 1,
    "scroll_delay": 1,
    "modal_delay": 1,        # 模态框出现等待时间
    "dropdown_delay": 1,     # 下拉框展开等待时间
    "log_loading_delay": 1,    # 日志加载等待时间
    "log_scroll_delay": 1,     # 日志滚动等待时间
}

# 检测结果等待配置
DETECTION_WAIT_CONFIG = {
    "max_wait_time": 5,  # 增加到2分钟
    "check_interval": 1,   # 每5秒检查一次
    "result_keywords_threshold": 2,
    "final_check_keywords": [
        "检测结果", "病害名称", "置信度", "建议", "检测完成",
        "detection", "result", "disease", "confidence", "complete"
    ]
}

# URL验证配置
URL_VALIDATION = {
    "login_success_patterns": [
        "/tabs/home",    # 主要的登录成功页面
        "/tabs/",        # 标签页根路径
        "/home"          # 备用路径
    ],
    "plot_detail_patterns": [
        "/tabs/strip/",
        "/plot/"
    ],
    "login_page_patterns": [
        "/login",
        "/signin"
    ]
}

# 元素选择器配置
SELECTORS = {
    "login": {
        "username": [
            "ion-input[label='用户名'] input",
            "ion-input[type='text'] input",
            "ion-item ion-input[type='text'] input",
            "input[type='text']",
            "#username",
            "[name='username']"
        ],
        "password": [
            "ion-input[label='密码'] input",
            "ion-input[type='password'] input", 
            "ion-item ion-input[type='password'] input",
            "input[type='password']",
            "#password",
            "[name='password']"
        ],
        "login_button": [
            "ion-button[expand='block']:not([fill='outline'])",  # 移除 :contains()
            "ion-button[type='submit']",
            "ion-button",
            "button[type='submit']",
            "[onclick*='login']"
        ],
        "signup_link": [
            "ion-button[router-link='/signup']",
            "ion-button[fill='outline']",
            "a[href*='signup']"
        ]
    },
    
    "plot_cards": [
        "ion-card[router-link*='/tabs/strip/']",  # 地块卡片的主要选择器（根据实际DOM）
        "ion-grid ion-row ion-col ion-card",     # 网格布局中的卡片
        "ion-col ion-card[button]",              # 带button属性的卡片
        "ion-card[button]",                      # 通用带button的卡片
        ".plot-card"                             # 备用选择器
    ],
    
    "plot_detail": {
        "more_options_button": [
            "#more-options-button",
            "ion-button[id='more-options-button']",
            "ion-buttons ion-button",
            "ion-header ion-buttons ion-button"
        ],
        "popover_menu": [
            "ion-popover ion-content",
            "ion-popover ion-list",
            "ion-list[role='menu']"
        ],
        "disease_detection_option": [
            "ion-item[button]",                      # 移除 :contains() 和 :has-text()
            "[data-testid='disease-detection']",
            "ion-item"                               # 通用选择器，通过JavaScript过滤文本
        ]
    },
    
    "disease_detection": {
        "modal": [
            "ion-modal[is-open='true']",
            "ion-modal .modal-wrapper",
            "ion-modal ion-content"
        ],
        "file_input": [
            "input[type='file']",
            "input[accept*='image']",
            "input[accept*='.jpg']"
        ],
        "submit_button": [
            "ion-button[expand='full']",             # 移除 :contains()
            "ion-button[type='submit']",
            "ion-button:not([disabled])",
            "ion-button"
        ],
        "close_button": [
            "ion-button",                            # 移除 :contains()
            "ion-buttons ion-button"
        ]
    },
    
    "error_messages": [
        "ion-alert .alert-message",
        "ion-toast .toast-message", 
        ".error-message",
        ".alert-danger",
        "[class*='error']",
        "[class*='alert']",
        "ion-card ion-card-content p",              # 移除 :contains()
        "ion-card ion-card-content div",            # 移除 :contains()
        "ion-alert .alert-button-inner",           # 添加更多有效选择器
        "ion-toast .toast-content",
        ".alert-message",
        ".error-text",
        "[role='alert']"
    ],
    
    "detection_result": [
        "ion-modal[is-open='true'] ion-card ion-card-title",  # 移除 :contains()
        "ion-modal ion-card ion-card-content",
        "ion-card ion-card-content",
        "ion-list ion-item",                                  # 移除 :contains()
        "[class*='detection-result']",
        "[data-testid*='result']"
    ],
    
    "weather_info": [
        "ion-card[style*='gradient']",
        "ion-card ion-card-title",                # 移除 :contains()
        "ion-card:first-child",
        ".weather-info",
        "[class*='weather']"
    ],
    
    "weather_elements": {
        "temperature": [
            "p:contains('°C')",                   # 包含摄氏度的段落
            "p:contains('气温')",                 # 包含"气温"的段落
            "[class*='temp']", 
            "[class*='temperature']"
        ],
        "weather_icon": [
            "ion-icon[icon*='sunny']",            # 天气图标
            "ion-icon[icon*='rainy']",
            "ion-icon[icon*='cloudy']",
            "ion-icon[color='primary']",          # 主色调图标
            "ion-icon"                            # 通用图标
        ],
        "location": [
            "ion-card-title:contains('当前天气')", # 城市天气标题
            "ion-card-title",                     # 卡片标题
            "[class*='location']", 
            "[class*='city']"
        ],
        "description": [
            "p:contains('天气')",                 # 包含"天气"的段落
            "ion-card-content p",                 # 卡片内容中的段落
            "[class*='desc']", 
            "[class*='condition']"
        ]
    },
    
    "ionic_ready": [
        "ion-app",
        "ion-content",
        "[ng-version]"
    ],
    
    "plot_creation": {
        "add_fab_button": [
            "ion-fab-button",
            "ion-fab ion-fab-button",
            "[data-testid='add-plot-button']"
        ],
        "modal": [
            "ion-modal[is-open='true']",
            "ion-modal .modal-wrapper"
        ],
        "plot_name_input": [
            "ion-modal ion-input[placeholder*='地块名称'] input",
            "ion-modal ion-input[v-model*='plotName'] input",
            "ion-modal ion-item ion-input input",
            "ion-input[placeholder*='请输入地块名称'] input",
            "ion-modal input[placeholder*='地块']"
        ],
        "plant_select": [
            "ion-modal ion-select[placeholder*='选择作物']",
            "ion-modal ion-select[v-model*='plantName']",
            "ion-modal ion-item ion-select",
            "ion-select[placeholder*='选择作物']",
            "ion-modal ion-select"
        ],
        "submit_button": [
            "ion-modal ion-button[expand='full']",
            "ion-modal ion-button:not([slot='end'])",
            "ion-modal ion-content ion-button",
            "ion-button[expand='full']"
        ],
        "close_button": [
            "ion-modal ion-buttons ion-button",
            "ion-buttons[slot='end'] ion-button"
        ]
    },
    
    "plot_logs": {
        "log_list": [
            "ion-list",
            "ion-content ion-list",
            "[class*='log-list']",
            "[data-testid='log-list']"
        ],
        "log_items": [
            "ion-list ion-item",
            "ion-item",
            ".log-item",
            "[class*='log-entry']"
        ],
        "log_content": [
            "ion-item ion-label",
            "ion-label",
            "ion-item p",
            ".log-content",
            ".log-text"
        ],
        "log_timestamp": [
            "ion-item ion-note",
            "ion-note",
            ".timestamp",
            ".log-time",
            "[class*='time']"
        ],
        "log_type": [
            "ion-item ion-badge",
            "ion-badge",
            ".log-type",
            ".log-category",
            "[class*='badge']"
        ],
        "empty_state": [
            "ion-card ion-card-content",
            ".empty-state",
            ".no-logs",
            "[class*='empty']"
        ]
    }
}

# JavaScript脚本配置
JAVASCRIPT_SCRIPTS = {
    "ionic_ready": """
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
    """,
    
    "scroll_to_element": "arguments[0].scrollIntoView(true);",
    
    "click_element": "arguments[0].click();",
    
    "set_input_value": "arguments[0].value = arguments[1];",
    
    "trigger_input_event": """
        var event = new Event('input', { bubbles: true });
        arguments[0].dispatchEvent(event);
    """,
    
    "find_weather_elements": """
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
    """,
    
    "find_disease_detection_options": """
        return Array.from(document.querySelectorAll('ion-item')).filter(
            el => el.textContent.includes('疾病检测') || 
                  el.textContent.includes('病害检测') ||
                  el.textContent.includes('检测')
        );
    """,
    
    "find_result_cards": """
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
    """,
    
    "find_login_elements": """
        return {
            username: document.querySelector('ion-input[label="用户名"] input') || 
                     document.querySelector('ion-input[type="text"] input') ||
                     document.querySelector('input[type="text"]'),
            password: document.querySelector('ion-input[label="密码"] input') || 
                     document.querySelector('ion-input[type="password"] input') ||
                     document.querySelector('input[type="password"]'),
            loginButton: Array.from(document.querySelectorAll('ion-button')).find(
                btn => btn.textContent.trim() === '登录' && !btn.getAttribute('fill')
            )
        };
    """,
    
    "check_home_page_loaded": """
        // 检查首页是否加载完成
        const indicators = [
            document.querySelector('ion-searchbar'),
            document.querySelector('ion-fab ion-fab-button'),
            document.querySelector('ion-grid'),
            document.querySelector('ion-card')
        ];
        
        return indicators.filter(el => el !== null).length >= 2;
    """,
    
    "find_weather_card": """
        // 查找天气卡片
        const cards = Array.from(document.querySelectorAll('ion-card'));
        return cards.find(card => {
            const content = card.textContent.toLowerCase();
            return content.includes('天气') || 
                   content.includes('气温') || 
                   content.includes('°c') ||
                   card.style.background.includes('gradient');
        });
    """,
    
    "find_plot_cards": """
        // 查找地块卡片
        return Array.from(document.querySelectorAll('ion-card[router-link*="/tabs/strip/"]'));
    """,
    
    "trigger_vue_input": """
        // 触发Vue的input事件
        var element = arguments[0];
        var value = arguments[1];
        
        // 设置值
        element.value = value;
        
        // 触发Vue的input事件
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        
        // 如果是Ionic组件，触发ionInput事件
        element.dispatchEvent(new CustomEvent('ionInput', { 
            detail: { value: value }, 
            bubbles: true 
        }));
    """,
    
    "click_vue_button": """
        // 点击Vue/Ionic按钮
        var button = arguments[0];
        
        // 触发点击事件
        button.click();
        
        // 如果是Ionic按钮，也触发ionClick事件
        button.dispatchEvent(new CustomEvent('ionClick', { bubbles: true }));
    """,
    
    # === 调试相关脚本 ===
    "debug_login_form": """
        // 调试登录表单状态
        var form = document.querySelector('form') || document.querySelector('ion-content');
        var inputs = Array.from(document.querySelectorAll('input'));
        var buttons = Array.from(document.querySelectorAll('ion-button'));
        
        var formData = {};
        inputs.forEach(function(input, index) {
            formData['input_' + index] = {
                type: input.type,
                value: input.value,
                name: input.name,
                placeholder: input.placeholder,
                disabled: input.disabled,
                visible: input.offsetParent !== null
            };
        });
        
        var buttonData = {};
        buttons.forEach(function(button, index) {
            buttonData['button_' + index] = {
                text: button.textContent.trim(),
                disabled: button.disabled,
                type: button.type,
                fill: button.getAttribute('fill'),
                expand: button.getAttribute('expand'),
                visible: button.offsetParent !== null
            };
        });
        
        return {
            formExists: !!form,
            inputCount: inputs.length,
            buttonCount: buttons.length,
            inputs: formData,
            buttons: buttonData,
            currentUrl: window.location.href,
            pageTitle: document.title
        };
    """,
    
    "monitor_vue_data": """
        // 监控Vue组件状态
        try {
            var vueElements = document.querySelectorAll('[data-v-]');
            var hasVue = vueElements.length > 0;
            
            var routerInfo = {};
            if (window.history && window.history.state) {
                routerInfo = window.history.state;
            }
            
            return {
                hasVueApp: hasVue,
                vueElementsCount: vueElements.length,
                routerState: routerInfo,
                currentPath: window.location.pathname,
                currentHash: window.location.hash
            };
        } catch(e) {
            console.log('Vue监控失败:', e);
            return { 
                hasVueApp: false, 
                error: e.message,
                currentPath: window.location.pathname 
            };
        }
    """,
    
    "enhanced_find_login_elements": """
        console.log('[DEBUG] 开始查找登录元素');
        
        // 查找用户名输入框
        var usernameSelectors = [
            'ion-input[label="用户名"] input',
            'ion-input[type="text"] input',
            'input[type="text"]'
        ];
        var usernameElement = null;
        for (var i = 0; i < usernameSelectors.length; i++) {
            usernameElement = document.querySelector(usernameSelectors[i]);
            if (usernameElement) {
                console.log('[DEBUG] 找到用户名输入框，选择器:', usernameSelectors[i]);
                break;
            }
        }
        
        // 查找密码输入框
        var passwordSelectors = [
            'ion-input[label="密码"] input',
            'ion-input[type="password"] input',
            'input[type="password"]'
        ];
        var passwordElement = null;
        for (var i = 0; i < passwordSelectors.length; i++) {
            passwordElement = document.querySelector(passwordSelectors[i]);
            if (passwordElement) {
                console.log('[DEBUG] 找到密码输入框，选择器:', passwordSelectors[i]);
                break;
            }
        }
        
        // 查找登录按钮
        var buttons = Array.from(document.querySelectorAll('ion-button'));
        console.log('[DEBUG] 找到', buttons.length, '个ion-button');
        
        var loginButton = null;
        for (var i = 0; i < buttons.length; i++) {
            var btn = buttons[i];
            var text = btn.textContent.trim();
            var fill = btn.getAttribute('fill');
            var expand = btn.getAttribute('expand');
            var disabled = btn.disabled;
            console.log('[DEBUG] 按钮', i, '- 文本:', text, ', fill:', fill, ', expand:', expand, ', disabled:', disabled);
            
            if (text === '登录' && (!fill || fill !== 'outline')) {
                loginButton = btn;
                console.log('[DEBUG] 选择登录按钮:', i);
                break;
            }
        }
        
        var result = {
            username: usernameElement,
            password: passwordElement,
            loginButton: loginButton
        };
        
        console.log('[DEBUG] 查找结果:', {
            username: !!result.username,
            password: !!result.password,
            loginButton: !!result.loginButton
        });
        
        return result;
    """,
    
    "simulate_user_login": """
        // 模拟真实用户登录行为
        var username = arguments[0];
        var password = arguments[1];
        
        console.log('[DEBUG] 开始模拟用户登录');
        
        // 查找元素
        var usernameInput = document.querySelector('ion-input[label="用户名"] input') || 
                           document.querySelector('input[type="text"]');
        var passwordInput = document.querySelector('ion-input[label="密码"] input') || 
                           document.querySelector('input[type="password"]');
        var loginButton = Array.from(document.querySelectorAll('ion-button')).find(
            btn => btn.textContent.trim() === '登录' && !btn.getAttribute('fill')
        );
        
        if (!usernameInput || !passwordInput || !loginButton) {
            return {
                success: false,
                error: '未找到必要元素',
                found: {
                    username: !!usernameInput,
                    password: !!passwordInput,
                    button: !!loginButton
                }
            };
        }
        
        try {
            // 1. 聚焦用户名输入框
            usernameInput.focus();
            
            // 2. 输入用户名
            usernameInput.value = username;
            usernameInput.dispatchEvent(new Event('input', { bubbles: true }));
            usernameInput.dispatchEvent(new Event('change', { bubbles: true }));
            usernameInput.dispatchEvent(new CustomEvent('ionInput', { detail: { value: username }, bubbles: true }));
            
            // 3. 聚焦密码输入框
            passwordInput.focus();
            
            // 4. 输入密码
            passwordInput.value = password;
            passwordInput.dispatchEvent(new Event('input', { bubbles: true }));
            passwordInput.dispatchEvent(new Event('change', { bubbles: true }));
            passwordInput.dispatchEvent(new CustomEvent('ionInput', { detail: { value: password }, bubbles: true }));
            
            // 5. 点击登录按钮
            loginButton.click();
            loginButton.dispatchEvent(new CustomEvent('ionClick', { bubbles: true }));
            
            return {
                success: true,
                message: '登录操作已执行',
                values: {
                    username: usernameInput.value,
                    password: passwordInput.value
                }
            };
            
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    """,
}

# 测试用例配置
TEST_CASES_CONFIG = {
    "plot_detection": {
        "test_id": "E2E_TC_001",
        "test_name": "地块检测完整流程测试",
        "test_purpose": "验证用户从登录到完成地块检测的完整业务流程",
        "test_steps": [
            "用户访问网站",
            "用户输入用户名密码并登录",
            "系统跳转到首页",
            "用户点击第一个地块卡片",
            "用户点击更多选项按钮",
            "用户选择疾病检测选项",
            "用户上传测试图片",
            "用户提交检测请求",
            "系统返回检测结果"
        ],
        "expected_result": "成功完成地块检测并获得结果",
        "test_type": "端到端测试",
        "priority": "高"
    },
    
    "weather_info": {
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
    },
    
    "plot_management": {
        "test_id": "E2E_TC_003",
        "test_name": "地块管理完整流程测试",
        "test_purpose": "验证用户创建地块和删除地块的完整业务流程",
        "test_steps": [
            "用户访问网站",
            "用户输入用户名密码并登录",
            "系统跳转到首页",
            "用户点击添加地块按钮",
            "用户填写地块名称",
            "用户选择第一种植物",
            "用户提交创建地块",
            "系统创建地块成功"
        ],
        "expected_result": "成功创建地块并成功删除地块",
        "test_type": "端到端测试",
        "priority": "高"
    },
    
    "plot_logs": {
        "test_id": "E2E_TC_004",
        "test_name": "地块日志查看测试",
        "test_purpose": "验证用户能够查看地块的历史日志记录",
        "test_method": "场景法",
        "precondition": "用户已有账户且存在地块数据",
        "test_steps": [
            "用户访问网站",
            "用户输入用户名密码并登录",
            "系统跳转到首页",
            "用户点击第一个地块卡片",
            "系统跳转到地块详情页",
            "系统显示地块日志列表",
            "验证日志内容完整性"
        ],
        "expected_result": "成功查看地块日志记录，日志内容完整且格式正确",
        "test_type": "端到端测试",
        "priority": "中"
    }
}

# 天气信息验证配置
WEATHER_VALIDATION = {
    "keywords": ["天气", "温度", "°C", "°F", "晴", "雨", "云", "weather", "temperature"],
    "error_keywords": ["检测失败", "处理失败", "错误", "失败", "error", "failed"],
    "result_keywords": ["结果", "检测", "分析", "完成", "result", "detection", "analysis"]
}

# 文件清理配置
CLEANUP_CONFIG = {
    "default_keep_recent": 5,
    "supported_image_formats": ['.png', '.jpg', '.jpeg'],
    "temp_file_prefix": "test_",
    "cleanup_types": ["screenshots", "logs", "temp_files"]
}

# 错误处理配置
ERROR_CODES = {
    "MISSING_PARAMS": "缺少请求参数",
    "CONFIG_VALIDATION_ERROR": "配置验证失败",
    "SYSTEM_ERROR": "系统错误",
    "GET_CASES_ERROR": "获取测试用例失败",
    "GET_WEATHER_CASES_ERROR": "获取天气测试用例失败",
    "VALIDATION_ERROR": "验证错误",
    "BAD_REQUEST": "请求格式错误",
    "NOT_FOUND": "请求的资源不存在",
    "INTERNAL_ERROR": "内部服务器错误"
}

# 调试配置
DEBUG_CONFIG = {
    "enable_detailed_logging": True,
    "save_debug_screenshots": True,
    "save_page_source": True,
    "monitor_network_requests": True,
    "log_browser_console": True,
    "debug_screenshot_interval": 2,  # 每2秒截图一次（调试模式）
    "max_debug_logs": 50
}

# 日志验证配置
LOG_VALIDATION = {
    "required_fields": ["timestamp", "content"],
    "optional_fields": ["type", "level", "category"],
    "min_log_count": 0,  # 最少日志条数（0表示允许空日志）
    "max_log_count": 100,  # 最多验证的日志条数
    "timestamp_formats": [
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%m-%d %H:%M",
        "%H:%M:%S"
    ],
    "content_keywords": [
        "检测", "病害", "上传", "创建", "删除", "修改",
        "detection", "disease", "upload", "create", "delete", "update"
    ]
}