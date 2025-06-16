from flask import Blueprint, request, jsonify
import importlib
import inspect
import os
import sys
import app.service.scan as scan_service
from app.service.unit import UnitTestService
from app.service.utils import ExcelTestCaseLoader,TestCaseObjectBuilder
import datetime
import pandas as pd
unit_bp = Blueprint("unit", __name__)


@unit_bp.route("/scan_classes", methods=["POST"])
def scan_directory():
    """
    扫描指定目录，返回 {类名: {方法名: [参数信息, ...]}} 的字典结构
    请求 JSON: { "directory": "路径" }
    """
    data = request.get_json()
    directory = data.get("directory")

    if not directory or not os.path.isdir(directory):
        return jsonify({"success": False, "message": "无效目录路径"}), 400

    class_map = scan_service.scan_classes_in_directory(directory)
    return jsonify({"success": True, "data": class_map})

@unit_bp.route("/scan_functions", methods=["POST"])
def scan_functions():
    data = request.get_json()
    directory = data.get("directory")

    if not directory or not os.path.exists(directory):
        return jsonify({"success": False, "error": "Invalid project directory"}), 400

    function_map = scan_service.scan_functions_in_directory(directory)
    return jsonify({"success": True, "data": function_map})


@unit_bp.route('/run_unit_test', methods=['POST'])
def run_unit_test():
    """
    执行单元测试接口

    请求参数:
    - root: 项目根路径
    - class_name: 类名（如 models.models.Disease）
    - method_name: 方法名（如 clone）
    - mock_config: Mock配置字典 {mock_target: mock_value} (可选)
    - excel_file: Excel文件（multipart/form-data）

    Excel文件格式：
    - 第一行：列名（ID、测试方法、测试描述、属性名等）
    - 第二行：数据类型（对应每列的数据类型）
    - 第三行开始：测试数据
    """

    try:
        root = request.form.get('root')
        class_name = request.form.get('class_name')
        method_name = request.form.get('method_name')
        mock_config = eval(request.form.get('mock_config', '{}'))  # Mock配置

        # 处理上传的Excel文件
        if 'excel_file' not in request.files:
            return jsonify({
                "success": False,
                "message": "缺少excel_file文件"
            }), 400

        excel_file = request.files['excel_file']
        if excel_file.filename == '':
            return jsonify({
                "success": False,
                "message": "未选择文件"
            }), 400

        # 保存上传的文件
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"test_cases_{timestamp}_{excel_file.filename}"
        excel_path = os.path.join('temp', filename)

        # 确保temp目录存在
        os.makedirs('temp', exist_ok=True)
        excel_file.save(excel_path)

        # 验证Mock配置格式
        if mock_config and not isinstance(mock_config, dict):
            return jsonify({
                "success": False,
                "message": "mock_config必须是字典格式"
            }), 400

        # 验证必要参数
        if not all([root, class_name, method_name]):
            return jsonify({
                "success": False,
                "message": "缺少必要参数: root, class_name, method_name"
            }), 400

        # 验证文件路径
        if not os.path.exists(excel_path):
            return jsonify({
                "success": False,
                "message": f"Excel文件不存在: {excel_path}"
            }), 400

        # 1. 加载Excel测试用例
        loader_result = ExcelTestCaseLoader.load_test_cases(excel_path)

        if not loader_result["success"]:
            return jsonify({
                "success": False,
                "message": f"Excel文件加载失败: {loader_result.get('message', '未知错误')}",
                "class": class_name,
                "method_name": method_name
            }), 400

        # 2. 获取测试用例和元信息
        test_cases = loader_result["test_cases"]
        test_method = loader_result["test_method"]
        test_name = loader_result["test_name"]
        description = loader_result["description"]
        param_types = loader_result["param_types"]  # 从Excel第二行获取的参数类型

        # 3. 数据类型转换
        # 3. 数据类型转换和对象构造
        try:
            converted_test_cases = TestCaseObjectBuilder.build_test_objects(
                test_cases,
                param_types,
                root  # 使用请求参数中的root作为项目根路径
            )
        except ValueError as e:
            return jsonify({
                "success": False,
                "message": f"数据类型转换失败: {str(e)}",
                "class": class_name,
                "method_name": method_name
            }), 400

        # 4. 调用service执行单元测试
        test_service = UnitTestService()
        test_result = test_service.execute_unit_test(
            root=root,
            class_name=class_name,
            method_name=method_name,
            test_cases=converted_test_cases,
            param_types=param_types,
            mock_config=mock_config  # 传递mock配置
        )

        # 5. 封装响应体
        response = {
            "success": test_result.get("success", False),
            "message": test_result.get("message", ""),
            "class": class_name,
            "method_name": method_name,
            "test_method": test_method,
            "test_name": test_name,
            "description": description,
            "mock_config": mock_config,  # 包含mock配置信息
            "summary": test_result.get("summary", {
                "total_cases": 0,
                "passed_cases": 0,
                "failed_cases": 0,
                "pass_rate": "0%"
            }),
            "test_results": test_result.get("test_results", [])
        }

        # 6. 清理临时文件（如果是上传的文件）
        if not request.is_json and os.path.exists(excel_path):
            try:
                os.remove(excel_path)
            except:
                pass  # 忽略删除失败

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"执行单元测试时发生错误: {str(e)}",
            "class": class_name,
            "method_name": request.get_json().get('method_name', '') if request.is_json else request.form.get(
                'method_name', '')
        }), 500
