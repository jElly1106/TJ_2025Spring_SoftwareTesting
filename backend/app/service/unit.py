import importlib
import inspect
import sys
import os
import time
import asyncio
from typing import Dict, Any, List, Tuple, Optional, Callable, Union
from unittest.mock import patch, MagicMock, AsyncMock
from contextlib import ExitStack


class UnitTestService:
    """单元测试服务类"""

    def __init__(self):
        self.module_cache = {}  # 模块缓存

    def execute_unit_test(self, root: str, class_name: str, method_name: str,
                          test_cases: List[Dict], param_types: Dict[str, str],
                          mock_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行单元测试主方法

        Args:
            root: 项目根路径
            class_name: 类名或模块路径 (如 models.models.Disease 或 utils.helpers)
            method_name: 方法名或函数名
            test_cases: 测试用例列表
            param_types: 参数类型字典
            mock_config: Mock配置字典

        Returns:
            测试结果字典
        """
        try:
            # 1. 添加项目根路径到系统路径
            if root not in sys.path:
                sys.path.insert(0, root)

            # 2. 解析目标路径
            target_type, module_path, target_name = self._parse_target(class_name, method_name)

            # 3. 导入目标对象
            target_callable, is_async = self._import_target(module_path, target_name, target_type)

            # 4. 执行测试用例
            test_results = []

            for test_case in test_cases:
                try:
                    # 设置Mock
                    with ExitStack() as stack:
                        if mock_config:
                            self._setup_mocks(mock_config, stack)

                        # 执行单个测试
                        if is_async:
                            result = asyncio.run(self._execute_single_test_async(
                                target_callable, test_case, param_types
                            ))
                        else:
                            result = self._execute_single_test(
                                target_callable, test_case, param_types
                            )
                        test_results.append(result)

                except Exception as e:
                    # 单个用例执行失败
                    test_results.append({
                        "ID": test_case.get("ID", "unknown"),
                        "Expected": test_case.get("期望结果", "N/A"),
                        "Actual": None,
                        "Passed": False,
                        "Duration": "0ms"
                    })

            # 5. 计算统计信息
            summary = self._calculate_summary(test_results)

            return {
                "success": True,
                "message": "单元测试执行完成",
                "summary": summary,
                "test_results": test_results
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"单元测试执行失败: {str(e)}",
                "summary": {
                    "total_cases": len(test_cases),
                    "passed_cases": 0,
                    "failed_cases": len(test_cases),
                    "pass_rate": "0%"
                },
                "test_results": []
            }

    def _parse_target(self, class_name: str, method_name: str) -> Tuple[str, str, str]:
        """
        解析目标路径

        Args:
            class_name: 类名或模块路径
            method_name: 方法名或函数名

        Returns:
            (target_type, module_path, target_name)
            target_type: 'class_method' | 'module_function'
        """
        parts = class_name.split('.')

        if len(parts) >= 3:
            # 假设是类方法: models.models.Disease
            module_path = '.'.join(parts[:-1])  # models.models
            class_name_only = parts[-1]  # Disease
            return 'class_method', module_path, f"{class_name_only}.{method_name}"
        else:
            # 假设是模块函数: utils.helpers
            module_path = class_name
            return 'module_function', module_path, method_name

    def _import_target(self, module_path: str, target_name: str, target_type: str) -> Tuple[Callable, bool]:
        """
        动态导入目标对象

        Args:
            module_path: 模块路径
            target_name: 目标名称
            target_type: 目标类型

        Returns:
            (可调用的目标对象, 是否为异步方法)
        """
        try:
            # 从缓存获取或导入模块
            if module_path not in self.module_cache:
                self.module_cache[module_path] = importlib.import_module(module_path)

            module = self.module_cache[module_path]

            if target_type == 'class_method':
                # 处理类方法
                class_name, method_name = target_name.split('.', 1)
                target_class = getattr(module, class_name)

                if not inspect.isclass(target_class):
                    raise ValueError(f"{class_name} 不是一个类")

                # 检查方法类型
                if hasattr(target_class, method_name):
                    method = getattr(target_class, method_name)

                    # 检查是否为异步方法
                    is_async_method = False
                    actual_method = method

                    if isinstance(method, staticmethod):
                        # 静态方法
                        actual_method = method.__func__
                        is_async_method = inspect.iscoroutinefunction(actual_method)
                        return actual_method, is_async_method
                    elif isinstance(method, classmethod):
                        # 类方法
                        actual_method = method.__func__
                        is_async_method = inspect.iscoroutinefunction(actual_method)
                        return lambda *args, **kwargs: actual_method(target_class, *args, **kwargs), is_async_method
                    else:
                        # 实例方法或普通方法
                        is_async_method = inspect.iscoroutinefunction(method)

                        if is_async_method:
                            # 异步实例方法
                            async def async_callable_wrapper(*args, **kwargs):
                                instance = target_class()
                                return await getattr(instance, method_name)(*args, **kwargs)

                            return async_callable_wrapper, True
                        else:
                            # 同步实例方法
                            def callable_wrapper(*args, **kwargs):
                                instance = target_class()
                                return getattr(instance, method_name)(*args, **kwargs)

                            return callable_wrapper, False
                else:
                    raise AttributeError(f"类 {class_name} 没有方法 {method_name}")

            elif target_type == 'module_function':
                # 处理模块函数
                if hasattr(module, target_name):
                    func = getattr(module, target_name)
                    if inspect.isfunction(func):
                        is_async_func = inspect.iscoroutinefunction(func)
                        return func, is_async_func
                    else:
                        raise ValueError(f"{target_name} 不是一个函数")
                else:
                    raise AttributeError(f"模块 {module_path} 没有函数 {target_name}")

            else:
                raise ValueError(f"不支持的目标类型: {target_type}")

        except ImportError as e:
            raise ImportError(f"无法导入模块 {module_path}: {str(e)}")
        except Exception as e:
            raise Exception(f"导入目标对象失败: {str(e)}")

    def _setup_mocks(self, mock_config: Dict[str, Any], stack: ExitStack):
        """
        设置Mock配置

        Args:
            mock_config: Mock配置字典
            stack: 上下文管理器栈
        """
        for mock_target, mock_value in mock_config.items():
            try:
                # 判断是否需要异步Mock
                is_async_mock = self._should_use_async_mock(mock_target, mock_value)

                # 创建Mock对象
                if is_async_mock:
                    if mock_value is None:
                        mock_obj = AsyncMock(return_value=None)
                    elif isinstance(mock_value, dict):
                        mock_obj = AsyncMock(return_value=mock_value['mock_value'])
                    elif isinstance(mock_value, (list, tuple)):
                        mock_obj = AsyncMock(return_value=mock_value)
                    else:
                        mock_obj = AsyncMock(return_value=mock_value)
                else:
                    if mock_value is None:
                        mock_obj = MagicMock(return_value=None)
                    elif isinstance(mock_value, dict):
                        mock_obj = MagicMock(return_value=mock_value['mock_value'])
                    elif isinstance(mock_value, (list, tuple)):
                        mock_obj = MagicMock(return_value=mock_value)
                    else:
                        mock_obj = MagicMock(return_value=mock_value)

                # 应用Mock
                patcher = patch(mock_target, mock_obj)
                stack.enter_context(patcher)

            except Exception as e:
                raise Exception(f"设置Mock失败 {mock_target}: {str(e)}")

    def _should_use_async_mock(self, mock_target: str, mock_value: Any) -> bool:
        """
        判断是否应该使用AsyncMock

        Args:
            mock_target: Mock目标
            mock_value: Mock值

        Returns:
            是否使用AsyncMock
        """
        # 简单的启发式规则：如果Mock目标包含常见的异步方法名称，使用AsyncMock
        async_indicators = ['async', 'await', 'coroutine', 'fetch', 'save', 'delete', 'create', 'update']
        target_lower = mock_target.lower()

        # 检查是否包含异步指示词
        for indicator in async_indicators:
            if indicator in target_lower:
                return True

        # 如果mock_value是特殊标记，也可以指示使用AsyncMock
        if isinstance(mock_value, dict) and mock_value.get('_async_mock', False):
            return True

        return False

    async def _execute_single_test_async(self, target_callable: Callable, test_case: Dict,
                                         param_types: Dict[str, str]) -> Dict[str, Any]:
        """
        执行单个异步测试用例

        Args:
            target_callable: 异步目标可调用对象
            test_case: 测试用例
            param_types: 参数类型字典

        Returns:
            测试结果字典
        """
        case_id = test_case.get("ID", "unknown")
        expected = test_case.get("期望结果", None)

        try:
            # 提取输入参数
            input_params = self._extract_input_params(test_case, param_types)

            # 记录开始时间
            start_time = time.time()

            # 调用异步目标方法
            actual = await self._call_target_method_async(target_callable, input_params)

            # 计算执行时间
            duration = f"{int((time.time() - start_time) * 1000)}ms"

            # 比较结果
            passed = self._compare_results(expected, actual)

            return {
                "ID": case_id,
                "Expected": expected,
                "Actual": actual,
                "Passed": passed,
                "Duration": duration
            }

        except Exception as e:
            return {
                "ID": case_id,
                "Expected": expected,
                "Actual": None,
                "Passed": False,
                "Duration": "0ms"
            }

    def _execute_single_test(self, target_callable: Callable, test_case: Dict,
                             param_types: Dict[str, str]) -> Dict[str, Any]:
        """
        执行单个测试用例

        Args:
            target_callable: 目标可调用对象
            test_case: 测试用例
            param_types: 参数类型字典

        Returns:
            测试结果字典
        """
        case_id = test_case.get("ID", "unknown")
        expected = test_case.get("期望结果", None)

        try:
            # 提取输入参数
            input_params = self._extract_input_params(test_case, param_types)

            # 记录开始时间
            start_time = time.time()

            # 调用目标方法
            actual = self._call_target_method(target_callable, input_params)

            # 计算执行时间
            duration = f"{int((time.time() - start_time) * 1000)}ms"

            # 比较结果
            passed = self._compare_results(expected, actual)

            return {
                "ID": case_id,
                "Expected": expected,
                "Actual": actual,
                "Passed": passed,
                "Duration": duration
            }

        except Exception as e:
            return {
                "ID": case_id,
                "Expected": expected,
                "Actual": None,
                "Passed": False,
                "Duration": "0ms"
            }

    def _extract_input_params(self, test_case: Dict, param_types: Dict[str, str]) -> Dict[str, Any]:
        """
        提取输入参数

        Args:
            test_case: 测试用例
            param_types: 参数类型字典

        Returns:
            输入参数字典
        """
        input_params = {}
        exclude_keys = {"ID", "期望结果", "测试方法", "测试名称", "测试描述"}

        for key, value in test_case.items():
            if key not in exclude_keys and key in param_types:
                input_params[key] = value

        return input_params

    async def _call_target_method_async(self, target_callable: Callable, params: Dict[str, Any]) -> Any:
        """
        调用异步目标方法

        Args:
            target_callable: 异步目标可调用对象
            params: 参数字典

        Returns:
            方法执行结果
        """
        try:
            # 获取方法签名
            sig = inspect.signature(target_callable)

            # 过滤有效参数
            valid_params = {}
            for param_name, param_value in params.items():
                if param_name in sig.parameters:
                    valid_params[param_name] = param_value

            # 异步调用方法
            return await target_callable(**valid_params)

        except TypeError as e:
            if "got an unexpected keyword argument" in str(e):
                # 尝试位置参数调用
                param_values = list(params.values())
                return await target_callable(*param_values)
            else:
                raise e

    def _call_target_method(self, target_callable: Callable, params: Dict[str, Any]) -> Any:
        """
        调用目标方法

        Args:
            target_callable: 目标可调用对象
            params: 参数字典

        Returns:
            方法执行结果
        """
        try:
            # 获取方法签名
            sig = inspect.signature(target_callable)

            # 过滤有效参数
            valid_params = {}
            for param_name, param_value in params.items():
                if param_name in sig.parameters:
                    valid_params[param_name] = param_value

            # 调用方法
            return target_callable(**valid_params)

        except TypeError as e:
            if "got an unexpected keyword argument" in str(e):
                # 尝试位置参数调用
                param_values = list(params.values())
                return target_callable(*param_values)
            else:
                raise e

    def _compare_results(self, expected: Any, actual: Any) -> bool:
        """
        比较期望结果和实际结果

        Args:
            expected: 期望结果
            actual: 实际结果

        Returns:
            是否匹配
        """
        try:
            # 处理None值
            if expected is None and actual is None:
                return True
            if expected is None or actual is None:
                return False

            # 字符串比较
            if isinstance(expected, str) and isinstance(actual, str):
                return expected.strip() == actual.strip()

            # 数值比较（处理浮点数精度问题）
            if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
                return abs(expected - actual) < 1e-9

            # 直接比较
            return expected == actual

        except Exception:
            return False

    def _calculate_summary(self, test_results: List[Dict]) -> Dict[str, Any]:
        """
        计算测试统计信息

        Args:
            test_results: 测试结果列表

        Returns:
            统计信息字典
        """
        total_cases = len(test_results)
        passed_cases = sum(1 for result in test_results if result.get("Passed", False))
        failed_cases = total_cases - passed_cases
        pass_rate = f"{(passed_cases / total_cases * 100):.1f}%" if total_cases > 0 else "0%"

        return {
            "total_cases": total_cases,
            "passed_cases": passed_cases,
            "failed_cases": failed_cases,
            "pass_rate": pass_rate
        }