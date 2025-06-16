import pandas as pd
import re
import importlib
from typing import Any, Dict, List, Type
import json

class ExcelTestCaseLoader:
    """Excel测试用例加载器"""

    @staticmethod
    def load_test_cases(file_path: str) -> Dict:
        """从Excel文件加载测试用例（新格式：第一行为列名，第二行为数据类型，第三行开始为测试数据）"""
        try:
            # 读取Excel文件，不设置header，保留原始行
            df_raw = pd.read_excel(file_path, header=None)

            if len(df_raw) < 3:
                raise ValueError("Excel文件至少需要3行：列名行、数据类型行、测试数据行")

            # 第一行作为列名
            columns = df_raw.iloc[0].tolist()

            # 第二行作为数据类型
            data_types = df_raw.iloc[1].tolist()

            # 第三行开始作为测试数据
            test_data = df_raw.iloc[2:].reset_index(drop=True)
            test_data.columns = columns

            # 检查必要的列
            required_columns = ["ID", "期望结果"]
            for col in required_columns:
                if col not in columns:
                    raise ValueError(f"Excel文件缺少必要的列: {col}")

            # 获取测试元信息（从第一个测试数据行获取）
            first_row = test_data.iloc[0] if len(test_data) > 0 else pd.Series()
            test_method = first_row.get("测试方法", "") if "测试方法" in columns else ""
            test_name = first_row.get("测试名称", "") if "测试名称" in columns else ""
            test_description = first_row.get("测试描述", "") if "测试描述" in columns else ""

            # 创建参数类型映射（排除系统列）
            system_columns = ['ID', '期望结果', '测试方法', '测试名称', '测试描述']
            param_types = {}

            for i, col in enumerate(columns):
                if col not in system_columns and i < len(data_types):
                    data_type = data_types[i]
                    if pd.notna(data_type) and data_type != '':
                        param_types[col] = str(data_type).strip()

            # 转换为字典列表，过滤掉空行
            test_cases = []
            for _, row in test_data.iterrows():
                # 跳过ID为空的行
                if pd.isna(row.get('ID')) or row.get('ID') == '':
                    continue
                test_cases.append(row.to_dict())

            return {
                "success": True,
                "test_method": test_method,
                "test_name": test_name,
                "description": test_description,
                "param_types": param_types,
                "test_cases": test_cases
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"读取Excel文件失败: {str(e)}",
                "param_types": {},
                "test_cases": []
            }





class DataTypeConverter:
    """数据类型转换器"""

    @staticmethod
    def parse_complex_type(type_str: str) -> tuple:
        """
        解析复杂类型字符串
        例如: 'list(models.models.User)' -> ('list', 'models.models.User')
        """
        # 匹配 container_type(inner_type) 格式
        match = re.match(r'^(\w+)\(([^)]+)\)$', type_str.strip())
        if match:
            container_type = match.group(1).lower()
            inner_type = match.group(2).strip()
            return container_type, inner_type
        return None, type_str

    @staticmethod
    def get_class_from_string(class_path: str, project_root: str = None) -> Type:
        """
        根据字符串路径获取类对象
        例如: 'models.models.User' -> User类

        Args:
            class_path: 类的完整路径，如 'models.models.User'
            project_root: 项目根路径，用于添加到sys.path
        """
        import sys
        import os

        # 如果提供了项目根路径，添加到sys.path
        if project_root and project_root not in sys.path:
            sys.path.insert(0, project_root)

        try:
            parts = class_path.split('.')
            module_path = '.'.join(parts[:-1])
            class_name = parts[-1]

            # 动态导入模块
            module = importlib.import_module(module_path)

            # 获取类
            cls = getattr(module, class_name)
            return cls
        except (ImportError, AttributeError) as e:
            raise ValueError(f"无法导入类 '{class_path}': {str(e)}. 请检查项目路径和类路径是否正确")
        finally:
            # 清理sys.path，避免污染（可选）
            if project_root and project_root in sys.path:
                try:
                    sys.path.remove(project_root)
                except ValueError:
                    pass  # 如果已经被移除则忽略

    @staticmethod
    def dict_to_object(data: Dict, target_class: Type) -> Any:
        """
        将字典转换为指定类的对象
        """
        try:
            # 尝试直接使用字典作为关键字参数构造对象
            return target_class(**data)
        except TypeError:
            try:
                # 如果直接构造失败，尝试只传递类构造函数需要的参数
                import inspect
                sig = inspect.signature(target_class.__init__)
                params = sig.parameters

                # 过滤出构造函数需要的参数
                filtered_data = {}
                for param_name in params:
                    if param_name != 'self' and param_name in data:
                        filtered_data[param_name] = data[param_name]

                return target_class(**filtered_data)
            except Exception as e:
                raise ValueError(f"无法将字典转换为 {target_class.__name__} 对象: {str(e)}")

    @staticmethod
    def convert_value(value: Any, target_type: str, project_root: str = None) -> Any:
        """将值转换为目标类型

        Args:
            value: 要转换的值
            target_type: 目标类型字符串
            project_root: 项目根路径，用于类导入
        """
        if value is None or value == '' or (isinstance(value, str) and value.lower() == 'none'):
            return None

        try:
            # 解析复杂类型
            container_type, inner_type = DataTypeConverter.parse_complex_type(target_type)

            if container_type:
                # 处理容器类型
                return DataTypeConverter._convert_container_type(value, container_type, inner_type, project_root)
            else:
                # 处理简单类型
                return DataTypeConverter._convert_simple_type(value, target_type, project_root)

        except (ValueError, TypeError, SyntaxError) as e:
            raise ValueError(f"无法将值 '{value}' 转换为类型 '{target_type}': {str(e)}")

    @staticmethod
    def _convert_container_type(value: Any, container_type: str, inner_type: str, project_root: str = None) -> Any:
        """转换容器类型"""
        if container_type == 'list':
            # 处理列表类型
            if isinstance(value, str):
                try:
                    # 尝试解析JSON格式的字符串
                    parsed_value = json.loads(value) if value.startswith('[') else [value]
                except json.JSONDecodeError:
                    # 如果JSON解析失败，尝试eval
                    parsed_value = eval(value) if value.startswith('[') else [value]
            elif isinstance(value, list):
                parsed_value = value
            else:
                parsed_value = [value]

            # 转换列表中的每个元素
            result = []
            for item in parsed_value:
                if '.' in inner_type:  # 类路径格式，如 models.models.User
                    target_class = DataTypeConverter.get_class_from_string(inner_type, project_root)
                    if isinstance(item, dict):
                        result.append(DataTypeConverter.dict_to_object(item, target_class))
                    else:
                        result.append(target_class(item))
                else:
                    # 简单类型
                    result.append(DataTypeConverter._convert_simple_type(item, inner_type, project_root))

            return result

        elif container_type == 'dict':
            # 处理字典类型
            if isinstance(value, str):
                try:
                    parsed_value = json.loads(value) if value.startswith('{') else {}
                except json.JSONDecodeError:
                    parsed_value = eval(value) if value.startswith('{') else {}
            else:
                parsed_value = dict(value) if not isinstance(value, dict) else value

            # 如果inner_type是类路径，转换字典为对象
            if '.' in inner_type:
                target_class = DataTypeConverter.get_class_from_string(inner_type, project_root)
                return DataTypeConverter.dict_to_object(parsed_value, target_class)

            return parsed_value

        else:
            raise ValueError(f"不支持的容器类型: {container_type}")

    @staticmethod
    def _convert_simple_type(value: Any, target_type: str, project_root: str = None) -> Any:
        """转换简单类型"""
        target_type_lower = target_type.lower()

        if target_type_lower in ['int', 'integer']:
            return int(float(value))  # 先转float再转int，处理Excel中的数字格式
        elif target_type_lower in ['float', 'double']:
            return float(value)
        elif target_type_lower in ['str', 'string']:
            return str(value)
        elif target_type_lower in ['bool', 'boolean']:
            if isinstance(value, str):
                return value.lower() in ['true', '1', 'yes', 'on']
            return bool(value)
        elif target_type_lower in ['list', 'array']:
            if isinstance(value, str):
                try:
                    return json.loads(value) if value.startswith('[') else [value]
                except json.JSONDecodeError:
                    return eval(value) if value.startswith('[') else [value]
            return list(value) if not isinstance(value, list) else value
        elif target_type_lower in ['dict', 'object']:
            if isinstance(value, str):
                try:
                    return json.loads(value) if value.startswith('{') else {}
                except json.JSONDecodeError:
                    return eval(value) if value.startswith('{') else {}
            return dict(value) if not isinstance(value, dict) else value
        elif '.' in target_type:
            # 处理类路径，如 models.models.User
            target_class = DataTypeConverter.get_class_from_string(target_type, project_root)
            if isinstance(value, dict):
                return DataTypeConverter.dict_to_object(value, target_class)
            else:
                return target_class(value)
        else:
            # 默认返回原值
            return value


class TestCaseObjectBuilder:
    """测试用例对象构造器"""

    @staticmethod
    def build_test_objects(test_cases: List[Dict], param_types: Dict[str, str], project_root: str = None) -> List[Dict]:
        """
        根据参数类型将测试用例字典转换为包含对象的字典

        Args:
            test_cases: 测试用例字典列表
            param_types: 参数类型映射
            project_root: 项目根路径，用于类导入

        Returns:
            转换后的测试用例列表
        """
        converted_test_cases = []

        for case in test_cases:
            converted_case = case.copy()

            # 系统字段不进行转换
            system_fields = ['ID', '期望结果', '测试方法', '测试名称', '测试描述']

            for param_name, param_type in param_types.items():
                if param_name in converted_case and param_name not in system_fields:
                    try:
                        # 跳过空值
                        if converted_case[param_name] is None or converted_case[param_name] == '':
                            continue

                        converted_case[param_name] = DataTypeConverter.convert_value(
                            converted_case[param_name],
                            param_type,
                            project_root
                        )
                    except ValueError as e:
                        raise ValueError(f"用例ID {case.get('ID', 'unknown')}, 参数 {param_name}: {str(e)}")

            converted_test_cases.append(converted_case)

        return converted_test_cases