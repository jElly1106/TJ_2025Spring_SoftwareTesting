from flask import Blueprint, request, jsonify
from app.service.admin_test import AdminTestService

admin_test_bp = Blueprint('admin_test', __name__)

'''
    测试add_package接口
'''

@admin_test_bp.route('/admin/test/add_package', methods=['POST'])
def test_add_package():
    """
    测试add_package接口
    
    请求体格式：
    {
        "test_cases": [
            {
                "test_id": "IT_TC_001_001",
                "test_purpose": "创建套餐",
                "case_id": "001",
                "packageName": "试用套餐",
                "price": 12.34,
                "sumNum": 100,
                "expected_status": 200,
                "expected_message": "套餐创建成功",
                "test_type": "有效等价类"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        if not data or 'test_cases' not in data:
            return jsonify({
                "success": False,
                "message": "缺少test_cases参数"
            }), 400
        
        test_service = AdminTestService()
        results = test_service.run_add_package_tests(data['test_cases'])
        
        return jsonify({
            "success": True,
            "test_results": results,
            "summary": test_service.generate_summary(results)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
        }), 500

@admin_test_bp.route('/admin/test/package_predefined_cases', methods=['GET'])
def get_predefined_test_cases():
    """
    获取预定义的测试用例
    """
    test_service = AdminTestService()
    return jsonify({
        "success": True,
        "test_cases": test_service.get_package_predefined_cases()
    })

@admin_test_bp.route('/admin/test/run_all_package_tests', methods=['POST'])
def run_all_package_tests():
    """
    自动化执行所有add_package预定义测试用例
    
    请求体格式（可选）：
    {
        "stop_on_failure": false  // 是否在失败时停止，默认false
    }
    """
    try:
        data = request.get_json() or {}
        stop_on_failure = data.get('stop_on_failure', False)
        
        test_service = AdminTestService()
        
        # 获取所有预定义的package测试用例
        package_cases = test_service.get_package_predefined_cases()
        
        # 执行测试
        results = test_service.run_package_tests_batch(
            package_cases, 
            stop_on_failure=stop_on_failure
        )
        
        return jsonify({
            "success": True,
            "test_module": "add_package",
            "total_cases": len(package_cases),
            "test_results": results["test_results"],
            "execution_info": results["execution_info"],
            "summary": test_service.generate_module_summary(results["test_results"], "add_package")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"add_package自动化测试执行失败: {str(e)}"
        }), 500

'''
    测试add_plant接口
'''
@admin_test_bp.route('/admin/test/add_plant', methods=['POST'])
def test_add_plant():
    """
    测试add_plant接口
    
    请求体格式：
    {
        "test_cases": [
            {
                "test_id": "IT_TC_002_001",
                "test_purpose": "添加植物",
                "case_id": "001",
                "plantName": "葡萄",
                "plantFeature": "葡萄是葡萄科葡萄属木质藤本植物...",
                "plantIconURL": "grapes.jpg",
                "expected_status": 200,
                "expected_message": "植物添加成功",
                "test_type": "有效等价类"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        if not data or 'test_cases' not in data:
            return jsonify({
                "success": False,
                "message": "缺少test_cases参数"
            }), 400
        
        test_service = AdminTestService()
        results = test_service.run_add_plant_tests(data['test_cases'])
        
        return jsonify({
            "success": True,
            "test_results": results,
            "summary": test_service.generate_summary(results)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
        }), 500

@admin_test_bp.route('/admin/test/plant_predefined_cases', methods=['GET'])
def get_plant_predefined_test_cases():
    """
    获取add_plant接口的预定义测试用例
    """
    test_service = AdminTestService()
    return jsonify({
        "success": True,
        "test_cases": test_service.get_plant_predefined_cases()
    })

@admin_test_bp.route('/admin/test/run_all_plant_tests', methods=['POST'])
def run_all_plant_tests():
    """
    自动化执行所有add_plant预定义测试用例
    
    请求体格式（可选）：
    {
        "stop_on_failure": false  // 是否在失败时停止，默认false
    }
    """
    try:
        data = request.get_json() or {}
        stop_on_failure = data.get('stop_on_failure', False)
        
        test_service = AdminTestService()
        
        # 获取所有预定义的plant测试用例
        plant_cases = test_service.get_plant_predefined_cases()
        
        # 执行测试
        results = test_service.run_plant_tests_batch(
            plant_cases, 
            stop_on_failure=stop_on_failure
        )
        
        return jsonify({
            "success": True,
            "test_module": "add_plant",
            "total_cases": len(plant_cases),
            "test_results": results["test_results"],
            "execution_info": results["execution_info"],
            "summary": test_service.generate_module_summary(results["test_results"], "add_plant")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"add_plant自动化测试执行失败: {str(e)}"
        }), 500

'''
    测试city_input接口
'''
@admin_test_bp.route('/admin/test/city_input', methods=['POST'])
def test_city_input():
    """
    测试city_input接口
    
    请求体格式：
    {
        "test_cases": [
            {
                "test_id": "IT_TC_003_001",
                "test_purpose": "导入城市",
                "case_id": "001",
                "csvURL": "data.csv",
                "expected_status": 200,
                "expected_message": "导入信息成功",
                "test_type": "有效等价类"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        if not data or 'test_cases' not in data:
            return jsonify({
                "success": False,
                "message": "缺少test_cases参数"
            }), 400
        
        test_service = AdminTestService()
        results = test_service.run_city_input_tests(data['test_cases'])
        
        return jsonify({
            "success": True,
            "test_results": results,
            "summary": test_service.generate_summary(results)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
        }), 500

@admin_test_bp.route('/admin/test/city_predefined_cases', methods=['GET'])
def get_city_predefined_cases():
    """
    获取预定义的城市导入测试用例
    """
    try:
        test_service = AdminTestService()
        cases = test_service.get_city_predefined_cases()
        
        return jsonify({
            "success": True,
            "test_cases": cases
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}"
        }), 500

@admin_test_bp.route('/admin/test/run_all_city_tests', methods=['POST'])
def run_all_city_tests():
    """
    自动执行所有城市导入预定义测试用例
    
    请求体格式：
    {
        "target_api": "http://47.120.78.249:8000/admin/weather/city_input",
        "stop_on_failure": false
    }
    """
    try:
        data = request.get_json() or {}
        target_api = data.get('target_api', 'http://47.120.78.249:8000/admin/weather/city_input')
        stop_on_failure = data.get('stop_on_failure', False)
        
        test_service = AdminTestService()
        results = test_service.run_city_tests_batch(target_api, stop_on_failure)
        
        return jsonify({
            "success": True,
            "test_results": results,
            "summary": test_service.generate_module_summary(results, "city_input")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"城市导入自动化测试执行失败: {str(e)}"
        }), 500


'''
    测试add_disease接口
'''

@admin_test_bp.route('/admin/test/disease_input', methods=['POST'])
def test_disease_input():
    """
    测试add_disease接口
    
    请求体格式：
    {
        "test_cases": [
            {
                "test_id": "IT_TC_004_001",
                "test_purpose": "正常添加病害",
                "case_id": "001",
                "diseaseName": "白粉病",
                "plantName": "小麦",
                "advice": "及时喷药治疗",
                "expected_status": 200,
                "expected_message": "病害添加成功",
                "test_type": "有效等价类"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        if not data or 'test_cases' not in data:
            return jsonify({
                "success": False,
                "message": "缺少test_cases参数"
            }), 400
        
        test_service = AdminTestService()
        results = test_service.run_disease_input_tests(data['test_cases'])
        
        return jsonify({
            "success": True,
            "test_results": results,
            "summary": test_service.generate_module_summary(results, "add_disease")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"测试执行失败: {str(e)}"
        }), 500

@admin_test_bp.route('/admin/test/disease_predefined_cases', methods=['GET'])
def get_disease_predefined_cases():
    """
    获取add_disease接口的预定义测试用例
    """
    try:
        test_service = AdminTestService()
        cases = test_service.get_disease_predefined_cases()
        
        return jsonify({
            "success": True,
            "test_cases": cases,
            "total_count": len(cases)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取预定义用例失败: {str(e)}"
        }), 500

@admin_test_bp.route('/admin/test/run_all_disease_tests', methods=['POST'])
def run_all_disease_tests():
    """
    执行所有add_disease预定义测试用例
    
    请求体格式（可选）：
    {
        "stop_on_failure": false
    }
    """
    try:
        data = request.get_json() or {}
        stop_on_failure = data.get('stop_on_failure', False)
        
        test_service = AdminTestService()
        predefined_cases = test_service.get_disease_predefined_cases()
        
        batch_result = test_service.run_disease_tests_batch(
            predefined_cases, 
            stop_on_failure=stop_on_failure
        )
        
        return jsonify({
            "success": True,
            "batch_result": batch_result,
            "summary": test_service.generate_module_summary(
                batch_result["test_results"], 
                "add_disease"
            )
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"批量测试执行失败: {str(e)}"
        }), 500