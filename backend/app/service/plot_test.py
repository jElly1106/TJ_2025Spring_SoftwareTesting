import requests
import time
from typing import List, Dict, Any

class PlotTestService:
    def __init__(self):
        # 目标API的基础URL
        self.base_url = "http://47.120.78.249:8000"
        # 用于认证的token，需要根据实际情况设置
        self.auth_token = None
    
    def set_auth_token(self, token: str):
        """设置认证token"""
        self.auth_token = token
    
    def get_auth_headers(self):
        """获取认证头"""
        if self.auth_token:
            return {"Authorization": f"Bearer {self.auth_token}"}
        return {}
    
    '''
        测试add_plot接口
    '''
    def get_plot_predefined_cases(self) -> List[Dict[str, Any]]:
        """
        返回add_plot接口的预定义测试用例
        """
        return [
            # 有效等价类测试
            {
                "test_id": "IT_TC_005_001",
                "test_purpose": "正常添加地块",
                "case_id": "001",
                "plotName": "地块A",
                "plantName": "水稻",
                "expected_status": 200,
                "expected_message": "地块创建成功",
                "test_type": "有效等价类"
            },
            # 无效等价类测试 - 参数为空
            {
                "test_id": "IT_TC_005_002",
                "test_purpose": "参数为空",
                "case_id": "001",
                "plotName": None,
                "plantName": "水稻",
                "expected_status": 422,
                "expected_message": "参数缺失",
                "test_type": "无效等价类"
            },
            {
                "test_id": "IT_TC_005_002",
                "test_purpose": "参数为空",
                "case_id": "002",
                "plotName": "地块A",
                "plantName": None,
                "expected_status": 422,
                "expected_message": "参数缺失",
                "test_type": "无效等价类"
            },
            # 无效等价类测试 - 用户未认证
            {
                "test_id": "IT_TC_005_003",
                "test_purpose": "用户未认证",
                "case_id": "001",
                "plotName": "地块A",
                "plantName": "水稻",
                "expected_status": 401,
                "expected_message": "未认证",
                "test_type": "无效等价类",
                "skip_auth": True
            },
            # 无效等价类测试 - 未知作物
            {
                "test_id": "IT_TC_005_004",
                "test_purpose": "未知作物",
                "case_id": "001",
                "plotName": "地块A",
                "plantName": "未知作物",
                "expected_status": 400,
                "expected_message": "作物不存在",
                "test_type": "无效等价类"
            },
            # 边界值分析测试
            {
                "test_id": "IT_TC_005_005",
                "test_purpose": "测试参数合法性",
                "case_id": "001",
                "plotName": "",  # 空字符串
                "plantName": "水稻",
                "expected_status": 400,
                "expected_message": "名称不能为空",
                "test_type": "边界值"
            },
            {
                "test_id": "IT_TC_005_005",
                "test_purpose": "测试参数合法性",
                "case_id": "002",
                "plotName": "A",  # 单字符
                "plantName": "水稻",
                "expected_status": 200,
                "expected_message": "地块创建成功",
                "test_type": "边界值"
            },
            {
                "test_id": "IT_TC_005_005",
                "test_purpose": "测试参数合法性",
                "case_id": "004",
                "plotName": "A" * 63,  # 63字符
                "plantName": "水稻",
                "expected_status": 200,
                "expected_message": "地块创建成功",
                "test_type": "边界值"
            },
            {
                "test_id": "IT_TC_005_005",
                "test_purpose": "测试参数合法性",
                "case_id": "005",
                "plotName": "A" * 65,  # 65字符
                "plantName": "水稻",
                "expected_status": 400,
                "expected_message": "参数超长",
                "test_type": "边界值"
            }
        ]
    
    def run_plot_input_tests(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行add_plot接口测试
        """
        results = []
        
        for test_case in test_cases:
            result = self._execute_plot_test(test_case)
            results.append(result)
            
        return results
    
    def _execute_plot_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个plot测试用例
        """
        start_time = time.time()
        
        try:
            # 构建请求数据
            data = {}
            if test_case.get('plotName') is not None:
                data['plotName'] = test_case['plotName']
            if test_case.get('plantName') is not None:
                data['plantName'] = test_case['plantName']
            
            # 设置请求头
            headers = {'Content-Type': 'application/json'}
            
            # 如果不跳过认证，添加认证头
            if not test_case.get('skip_auth', False):
                headers.update(self.get_auth_headers())
            
            # 发送请求
            response = requests.post(
                f"{self.base_url}/plot/add",
                json=data,
                headers=headers,
                timeout=10
            )
            
            # 计算执行时间
            duration = round((time.time() - start_time) * 1000, 2)  # 毫秒
            
            # 分析结果
            actual_status = response.status_code
            expected_status = test_case['expected_status']
            
            try:
                response_data = response.json()
                actual_message = response_data.get('message', response_data.get('detail', ''))
            except:
                actual_message = response.text
            
            # 判断是否通过
            status_match = actual_status == expected_status
            message_match = test_case['expected_message'] in actual_message
            passed = status_match and message_match
            
            return {
                "test_id": test_case['test_id'],
                "test_purpose": test_case['test_purpose'],
                "case_id": test_case['case_id'],
                "test_type": test_case['test_type'],
                "input_params": {
                    "plotName": test_case.get('plotName'),
                    "plantName": test_case.get('plantName')
                },
                "expected_status": expected_status,
                "actual_status": actual_status,
                "expected_message": test_case['expected_message'],
                "actual_message": actual_message,
                "passed": passed,
                "duration_ms": duration,
                "error": None
            }
            
        except Exception as e:
            duration = round((time.time() - start_time) * 1000, 2)
            return {
                "test_id": test_case['test_id'],
                "test_purpose": test_case['test_purpose'],
                "case_id": test_case['case_id'],
                "test_type": test_case['test_type'],
                "input_params": {
                    "plotName": test_case.get('plotName'),
                    "plantName": test_case.get('plantName')
                },
                "expected_status": test_case['expected_status'],
                "actual_status": None,
                "expected_message": test_case['expected_message'],
                "actual_message": str(e),
                "passed": False,
                "duration_ms": duration,
                "error": str(e)
            }
    
    def run_plot_tests_batch(self, test_cases, stop_on_failure=False):
        """
        批量执行add_plot测试用例
        
        Args:
            test_cases: 测试用例列表
            stop_on_failure: 是否在失败时停止执行
        
        Returns:
            Dict: 包含测试结果和执行信息的字典
        """
        execution_info = {
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stopped_early": False,
            "stop_reason": None,
            "module": "add_plot"
        }
        
        results = []
        
        try:
            print(f"开始执行add_plot模块测试，共{len(test_cases)}个用例...")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"执行add_plot测试 {i}/{len(test_cases)}: {test_case['test_id']} - {test_case['test_purpose']}")
                
                result = self._execute_plot_test(test_case)
                results.append(result)
                
                # 输出测试结果
                status = "✓ 通过" if result.get('passed') else "✗ 失败"
                print(f"  结果: {status} (耗时: {result.get('duration_ms', 0)}ms)")

                # 检查是否需要在失败时停止
                if stop_on_failure and not result.get('passed'):
                    execution_info["stopped_early"] = True
                    execution_info["stop_reason"] = f"测试用例失败: {test_case['test_id']}"
                    print(f"  ⚠️ 检测到失败，停止执行")
                    break
            
            execution_info["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"add_plot模块测试完成")
            
        except Exception as e:
            execution_info["stopped_early"] = True
            execution_info["stop_reason"] = f"执行异常: {str(e)}"
            execution_info["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"add_plot模块测试异常: {str(e)}")
        
        return {
            "test_results": results,
            "execution_info": execution_info
        }

    '''
        测试get_plot_detail接口
    '''
    def get_plot_detail_predefined_cases(self) -> List[Dict[str, Any]]:
        """
        返回get_plot_detail接口的预定义测试用例
        """
        return [
            # 有效等价类测试
            {
                "test_id": "IT_TC_006_001",
                "test_purpose": "正常获取地块详情",
                "case_id": "001",
                "plotId": "存在的合法ID",
                "user_status": "已登录",
                "expected_status": 200,
                "expected_message": "返回PlotDetails",
                "test_type": "有效等价类"
            },
            # 无效等价类测试
            {
                "test_id": "IT_TC_006_002",
                "test_purpose": "地块不存在",
                "case_id": "001",
                "plotId": "不存在的ID",
                "user_status": "已登录",
                "expected_status": 404,
                "expected_message": "地块不存在",
                "test_type": "无效等价类"
            },
            {
                "test_id": "IT_TC_006_003",
                "test_purpose": "用户未登录",
                "case_id": "001",
                "plotId": "合法ID",
                "user_status": "未登录",
                "expected_status": 401,
                "expected_message": "无权限",
                "test_type": "无效等价类",
                "skip_auth": True
            },
            {
                "test_id": "IT_TC_006_004",
                "test_purpose": "ID为null",
                "case_id": "001",
                "plotId": None,
                "user_status": "已登录",
                "expected_status": 422,
                "expected_message": "参数缺失",
                "test_type": "无效等价类"
            },
            # 边界值分析测试
            {
                "test_id": "IT_TC_006_005",
                "test_purpose": "参数合法性",
                "case_id": "001",
                "plotId": "",  # 空字符串
                "user_status": "已登录",
                "expected_status": 422,
                "expected_message": "参数格式错误",
                "test_type": "边界值"
            },
            {
                "test_id": "IT_TC_006_005",
                "test_purpose": "参数合法性",
                "case_id": "002",
                "plotId": "*恰好等于限制长度的ID",  # 标准UUID长度
                "user_status": "已登录",
                "expected_status": 200,
                "expected_message": "返回PlotDetails",
                "test_type": "边界值"
            },
            {
                "test_id": "IT_TC_006_005",
                "test_purpose": "参数合法性",
                "case_id": "003",
                "plotId": "*超过限制长度的ID",  # 超长ID
                "user_status": "已登录",
                "expected_status": 422,
                "expected_message": "参数格式错误",
                "test_type": "边界值"
            }
        ]
    
    def run_plot_detail_input_tests(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行get_plot_detail接口测试
        """
        results = []
        
        for test_case in test_cases:
            result = self._execute_plot_detail_test(test_case)
            results.append(result)
            
        return results
    
    def _execute_plot_detail_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个get_plot_detail测试用例
        """
        start_time = time.time()
        
        try:
            # 处理特殊测试用例的plotId
            plot_id = test_case.get('plotId')
            
            if plot_id == "存在的合法ID":
                # 这里需要替换为实际存在的地块ID，或者先创建一个地块
                plot_id = "123e4567-e89b-12d3-a456-426614174000"  # 示例UUID
            elif plot_id == "不存在的ID":
                plot_id = "999e9999-e99b-99d9-a999-999999999999"  # 不存在的UUID
            elif plot_id == "合法ID":
                plot_id = "123e4567-e89b-12d3-a456-426614174000"  # 示例UUID
            elif plot_id == "*恰好等于限制长度的ID":
                plot_id = "123e4567-e89b-12d3-a456-426614174000"  # 标准UUID长度
            elif plot_id == "*超过限制长度的ID":
                plot_id = "invalid-very-long-id-that-exceeds-normal-uuid-length-limits-and-more"
            
            # 设置请求头
            headers = {'Content-Type': 'application/json'}
            
            # 如果不跳过认证，添加认证头
            if not test_case.get('skip_auth', False):
                headers.update(self.get_auth_headers())
            
            # 构建请求URL
            if plot_id is None:
                # 测试缺少参数的情况
                url = f"{self.base_url}/plot/"
            else:
                url = f"{self.base_url}/plot/{plot_id}"
            
            # 发送GET请求
            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )
            
            # 计算执行时间
            duration = round((time.time() - start_time) * 1000, 2)  # 毫秒
            
            # 分析结果
            actual_status = response.status_code
            expected_status = test_case['expected_status']
            
            try:
                response_data = response.json()
                actual_message = response_data.get('message', response_data.get('detail', ''))
                # 如果是成功响应，检查返回的数据结构
                if actual_status == 200:
                    if 'plotId' in response_data and 'plotName' in response_data:
                        actual_message = "返回PlotDetails"
                    else:
                        actual_message = "返回数据格式错误"
            except:
                actual_message = response.text
            
            # 判断是否通过
            status_match = actual_status == expected_status
            message_match = test_case['expected_message'] in actual_message
            passed = status_match and message_match
            
            return {
                "test_id": test_case['test_id'],
                "test_purpose": test_case['test_purpose'],
                "case_id": test_case['case_id'],
                "test_type": test_case['test_type'],
                "input_params": {
                    "plotId": test_case.get('plotId'),
                    "user_status": test_case.get('user_status')
                },
                "expected_status": expected_status,
                "actual_status": actual_status,
                "expected_message": test_case['expected_message'],
                "actual_message": actual_message,
                "passed": passed,
                "duration_ms": duration,
                "error": None
            }
            
        except Exception as e:
            duration = round((time.time() - start_time) * 1000, 2)
            return {
                "test_id": test_case['test_id'],
                "test_purpose": test_case['test_purpose'],
                "case_id": test_case['case_id'],
                "test_type": test_case['test_type'],
                "input_params": {
                    "plotId": test_case.get('plotId'),
                    "user_status": test_case.get('user_status')
                },
                "expected_status": test_case['expected_status'],
                "actual_status": None,
                "expected_message": test_case['expected_message'],
                "actual_message": str(e),
                "passed": False,
                "duration_ms": duration,
                "error": str(e)
            }
    
    def run_plot_detail_tests_batch(self, test_cases=None, stop_on_failure=False):
        """
        批量执行get_plot_detail测试用例
        
        Args:
            test_cases: 测试用例列表，如果为None则使用预定义用例
            stop_on_failure: 是否在失败时停止执行
        
        Returns:
            Dict: 包含测试结果和执行信息的字典
        """
        if test_cases is None:
            test_cases = self.get_plot_detail_predefined_cases()
        
        execution_info = {
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "stopped_early": False,
            "stop_reason": None,
            "module": "get_plot_detail"
        }
        
        results = []
        
        try:
            print(f"开始执行get_plot_detail模块测试，共{len(test_cases)}个用例...")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"执行get_plot_detail测试 {i}/{len(test_cases)}: {test_case['test_id']} - {test_case['test_purpose']}")
                
                result = self._execute_plot_detail_test(test_case)
                results.append(result)
                
                # 输出测试结果
                status = "✓ 通过" if result.get('passed') else "✗ 失败"
                print(f"  结果: {status} (耗时: {result.get('duration_ms', 0)}ms)")

                # 检查是否需要在失败时停止
                if stop_on_failure and not result.get('passed'):
                    execution_info["stopped_early"] = True
                    execution_info["stop_reason"] = f"测试用例失败: {test_case['test_id']}"
                    print(f"  ⚠️ 检测到失败，停止执行")
                    break
            
            execution_info["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"get_plot_detail模块测试完成")
            
        except Exception as e:
            execution_info["stopped_early"] = True
            execution_info["stop_reason"] = f"执行异常: {str(e)}"
            execution_info["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"get_plot_detail模块测试异常: {str(e)}")
        
        return {
            "test_results": results,
            "execution_info": execution_info
        }


    def generate_module_summary(self, results: List[Dict[str, Any]], module_name: str) -> Dict[str, Any]:
        """
        生成模块测试总结
        """
        total_cases = len(results)
        passed_cases = sum(1 for r in results if r.get('passed', False))
        failed_cases = total_cases - passed_cases
        
        # 按测试类型分组统计
        type_stats = {}
        for result in results:
            test_type = result.get('test_type', '未知')
            if test_type not in type_stats:
                type_stats[test_type] = {'total': 0, 'passed': 0}
            type_stats[test_type]['total'] += 1
            if result.get('passed', False):
                type_stats[test_type]['passed'] += 1
        
        # 计算平均响应时间
        response_times = [r.get('duration_ms', 0) for r in results if r.get('duration_ms') is not None]
        avg_response_time = round(sum(response_times) / len(response_times), 2) if response_times else 0
        
        # 失败用例详情
        failed_cases_detail = []
        for r in results:
            if not r.get('passed', False):
                failed_cases_detail.append({
                    'test_id': r.get('test_id'),
                    'test_purpose': r.get('test_purpose'),
                    'expected_status': r.get('expected_status'),
                    'actual_status': r.get('actual_status'),
                    'expected_message': r.get('expected_message'),
                    'actual_message': r.get('actual_message'),
                    'error_message': r.get('error')
                })
        
        return {
            'module_name': module_name,
            'total_cases': total_cases,
            'passed_cases': passed_cases,
            'failed_cases': failed_cases,
            'pass_rate': round((passed_cases / total_cases) * 100, 2) if total_cases > 0 else 0,
            'avg_response_time_ms': avg_response_time,
            'type_statistics': type_stats,
            'failed_cases_detail': failed_cases_detail
        }