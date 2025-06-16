import inspect
import ast
import os
import sys
import importlib


def serialize_param(param: inspect.Parameter) -> dict:
    """将参数对象序列化为可 JSON 化的字典"""
    return {
        "name": param.name,
        "default": None if param.default == inspect.Parameter.empty else str(param.default),
        "annotation": None if param.annotation == inspect.Parameter.empty else str(param.annotation),
        "kind": str(param.kind)
    }


def attach_parents(tree):
    """给 AST 节点添加 parent 属性"""
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

def is_top_level_function(node):
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and isinstance(getattr(node, 'parent', None), ast.Module)


def extract_function_info(file_path, module_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    try:
        tree = ast.parse(source, filename=file_path)
        attach_parents(tree)
    except SyntaxError:
        return {}

    functions = []
    for node in ast.walk(tree):
        if is_top_level_function(node):
            arg_names = [arg.arg for arg in node.args.args]
            functions.append({
                "name": node.name,
                "args": arg_names,
                "async": isinstance(node, ast.AsyncFunctionDef)
            })

    return {module_name: functions} if functions else {}
EXCLUDE_DIRS = {'.venv', '__pycache__', 'site-packages'}

def scan_classes_in_directory(directory: str) -> dict[str, dict]:
    """
    实际执行扫描目录，返回 {类名: {方法名: [参数信息, ...]}} 结构
    """
    class_map = {}

    if directory not in sys.path:
        sys.path.insert(0, directory)

    for root, dirs, files in os.walk(directory):
        # 排除目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, directory)
                module_name = rel_path[:-3].replace(os.sep, '.')

                try:
                    module = importlib.import_module(module_name)
                except Exception as e:
                    print(f"Error loading {module_name}: {e}")
                    continue

                for cls_name, cls_obj in inspect.getmembers(module, inspect.isclass):
                    if cls_obj.__module__ != module.__name__:
                        continue

                    method_map = {}
                    for method_name, method_obj in inspect.getmembers(cls_obj, inspect.isfunction):
                        if method_name.startswith('_'):
                            continue

                        try:
                            sig = inspect.signature(method_obj)
                            param_list = []
                            for param in sig.parameters.values():
                                if param.name in ('self', 'cls'):
                                    continue
                                param_list.append(serialize_param(param))
                            method_map[method_name] = param_list
                        except Exception as e:
                            method_map[method_name] = [{"error": str(e)}]

                    full_class_name = f"{module_name}.{cls_name}"
                    class_map[full_class_name] = method_map

    return class_map

def scan_functions_in_directory(root_dir):
    function_map = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 排除虚拟环境目录
        if any(exclude in dirpath for exclude in ['.venv', '__pycache__', 'site-packages']):
            continue

        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(file_path, root_dir).replace(os.path.sep, ".").rstrip(".py")
                module_name = rel_path[:-3] if rel_path.endswith(".py") else rel_path

                result = extract_function_info(file_path, module_name)
                function_map.update(result)

    return function_map