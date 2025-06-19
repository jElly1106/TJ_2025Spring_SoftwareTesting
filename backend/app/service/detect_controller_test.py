import time
import inspect
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

# 模拟数据模型
@dataclass
class User:
    userId: str
    username: str
    email: str

@dataclass
class Plot:
    plotId: str
    plotName: str
    userId: User
    plantId: str
    createdAt: str

class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class DetectTestService:
    def __init__(self):
        # 模拟数据库数据
        self.mock_users = {
            "user_123": User(userId="user_123", username="testuser1", email="test1@example.com"),
            "user_456": User(userId="user_456", username="testuser2", email="test2@example.com"),
            "user_789": User(userId="user_789", username="testuser3", email="test3@example.com")
        }
        
        self.mock_plots = {
            "valid_plot_id_123": Plot(
                plotId="valid_plot_id_123",
                plotName="测试地块1",
                userId=self.mock_users["user_123"],
                plantId="plant_001",
                createdAt="2024-01-01"
            ),
            "unauthorized_plot_456": Plot(
                plotId="unauthorized_plot_456",
                plotName="测试地块2",
                userId=self.mock_users["user_456"],
                plantId="plant_002",
                createdAt="2024-01-02"
            ),
            "plot_id_normal_length_123456": Plot(
                plotId="plot_id_normal_length_123456",
                plotName="正常长度地块",
                userId=self.mock_users["user_789"],
                plantId="plant_003",
                createdAt="2024-01-03"
            )
        }
        
        # 当前认证用户
        self.current_user = None
    
    def set_current_user(self, user_id: str):
        """设置当前认证用户"""
        if user_id in self.mock_users:
            self.current_user = self.mock_users[user_id]
        else:
            self.current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """获取当前认证用户"""
        return self.current_user
    
    async def get_plot_by_id(self, plotId: str) -> Plot:
        """模拟获取地块信息"""
        if plotId in self.mock_plots:
            return self.mock_plots[plotId]
        else:
            raise Exception(f"地块 {plotId} 不存在")
    
    async def validate_plot_access(self, plotId: str, user: Optional[User] = None) -> Plot:
        """
        验证地块访问权限的核心函数
        这是被测试的目标函数
        """
        # 如果没有提供用户，使用当前认证用户
        if user is None:
            user = self.get_current_user()
        
        # 检查用户是否已认证
        if user is None:
            raise HTTPException(status_code=401, detail="未认证")
        
        # 验证地块访问权限
        try:
            plot = await self.get_plot_by_id(plotId)
            if plot.userId.userId != user.userId:
                raise HTTPException(status_code=403, detail="未授权的地块访问")
            return plot
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=404, detail=f"地块验证失败: {str(e)}")
    
    def get_function_source_code(self) -> Dict[str, str]:
        """
        获取 validate_plot_access 函数的源代码
        """
        try:
            # 获取函数源代码
            source_code = inspect.getsource(self.validate_plot_access)
            
            # 获取函数签名
            signature = str(inspect.signature(self.validate_plot_access))
            
            # 获取函数文档字符串
            docstring = inspect.getdoc(self.validate_plot_access) or "无文档字符串"
            
            return {
                "function_name": "validate_plot_access",
                "signature": f"async def validate_plot_access{signature}",
                "source_code": source_code,
                "docstring": docstring,
                "file_location": __file__,
                "line_number": inspect.getsourcelines(self.validate_plot_access)[1]
            }
        except Exception as e:
            return {
                "error": f"获取源代码失败: {str(e)}"
            }
    
    def get_validate_plot_access_predefined_cases(self) -> List[Dict[str, Any]]:
        """
        返回validate_plot_access函数的预定义测试用例
        """
        return [
            # 有效等价类测试
            {
                "test_id": "IT_TC_007_001",
                "test_purpose": "有效地块ID，授权用户访问",
                "case_id": "001",
                "plotId": "valid_plot_id_123",
                "userId": "user_123",
                "expected_status": 200,
                "expected_message": "验证成功",
                "test_type": "有效等价类",
                "description": "测试用户对自己拥有的地块的访问权限"
            },
            
            # 无效等价类测试 - 地块不存在
            {
                "test_id": "IT_TC_007_002",
                "test_purpose": "地块不存在",
                "case_id": "001",
                "plotId": "non_existent_plot_999",
                "userId": "user_123",
                "expected_status": 404,
                "expected_message": "地块验证失败",
                "test_type": "无效等价类",
                "description": "测试访问不存在的地块ID"
            },
            
            # 无效等价类测试 - 未授权访问
            {
                "test_id": "IT_TC_007_003",
                "test_purpose": "未授权的地块访问",
                "case_id": "001",
                "plotId": "unauthorized_plot_456",
                "userId": "user_123",  # user_123 尝试访问 user_456 的地块
                "expected_status": 403,
                "expected_message": "未授权的地块访问",
                "test_type": "无效等价类",
                "description": "测试用户访问其他用户的地块"
            },
            
            # 无效等价类测试 - 用户未认证
            {
                "test_id": "IT_TC_007_004",
                "test_purpose": "用户未认证",
                "case_id": "001",
                "plotId": "valid_plot_id_123",
                "userId": None,  # 未认证用户
                "expected_status": 401,
                "expected_message": "未认证",
                "test_type": "无效等价类",
                "skip_auth": True,
                "description": "测试未认证用户的访问"
            },
            
            # 无效等价类测试 - 空值测试
            {
                "test_id": "IT_TC_007_005",
                "test_purpose": "plotId为空值",
                "case_id": "001",
                "plotId": None,
                "userId": "user_123",
                "expected_status": 404,
                "expected_message": "地块验证失败",
                "test_type": "无效等价类",
                "description": "测试plotId参数为None的情况"
            },
            {
                "test_id": "IT_TC_007_005",
                "test_purpose": "plotId为空字符串",
                "case_id": "002",
                "plotId": "",
                "userId": "user_123",
                "expected_status": 404,
                "expected_message": "地块验证失败",
                "test_type": "无效等价类",
                "description": "测试plotId参数为空字符串的情况"
            },
            
            # 边界值分析测试
            {
                "test_id": "IT_TC_007_006",
                "test_purpose": "plotId长度边界值测试 - 最小长度",
                "case_id": "001",
                "plotId": "1",  # 最小长度
                "userId": "user_123",
                "expected_status": 404,
                "expected_message": "地块验证失败",
                "test_type": "边界值",
                "description": "测试单字符plotId"
            },
            {
                "test_id": "IT_TC_007_006",
                "test_purpose": "plotId长度边界值测试 - 正常长度",
                "case_id": "002",
                "plotId": "plot_id_normal_length_123456",  # 正常长度
                "userId": "user_789",  # 对应的用户
                "expected_status": 200,
                "expected_message": "验证成功",
                "test_type": "边界值",
                "description": "测试正常长度的plotId"
            },
            {
                "test_id": "IT_TC_007_006",
                "test_purpose": "plotId长度边界值测试 - 超长字符串",
                "case_id": "003",
                "plotId": "a" * 1000,  # 超长字符串
                "userId": "user_123",
                "expected_status": 404,
                "expected_message": "地块验证失败",
                "test_type": "边界值",
                "description": "测试超长plotId字符串"
            },
            
            # 特殊字符测试
            {
                "test_id": "IT_TC_007_007",
                "test_purpose": "plotId特殊字符测试",
                "case_id": "001",
                "plotId": "plot@#$%^&*()",
                "userId": "user_123",
                "expected_status": 404,
                "expected_message": "地块验证失败",
                "test_type": "边界值",
                "description": "测试包含特殊字符的plotId"
            },
            {
                "test_id": "IT_TC_007_007",
                "test_purpose": "plotId SQL注入测试",
                "case_id": "002",
                "plotId": "'; DROP TABLE plots; --",
                "userId": "user_123",
                "expected_status": 404,
                "expected_message": "地块验证失败",
                "test_type": "边界值",
                "description": "测试SQL注入攻击字符串"
            },
            {
                "test_id": "IT_TC_007_007",
                "test_purpose": "plotId Unicode字符测试",
                "case_id": "003",
                "plotId": "地块编号_测试_123",
                "userId": "user_123",
                "expected_status": 404,
                "expected_message": "地块验证失败",
                "test_type": "边界值",
                "description": "测试包含Unicode字符的plotId"
            }
        ]
    
    async def run_validate_plot_access_tests(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        运行validate_plot_access测试用例（直接调用函数）
        """
        results = []
        for test_case in test_cases:
            result = await self._execute_validate_plot_access_test(test_case)
            results.append(result)
            time.sleep(0.1)  # 短暂延迟
        return results
    
    async def _execute_validate_plot_access_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个validate_plot_access测试用例（直接调用函数）
        """
        start_time = time.time()
        
        try:
            # 设置当前用户
            if test_case.get('skip_auth', False):
                self.set_current_user(None)
            else:
                user_id = test_case.get('userId')
                if user_id:
                    self.set_current_user(user_id)
                else:
                    self.set_current_user(None)
            
            # 调用被测试的函数
            plot_id = test_case.get('plotId')
            result = await self.validate_plot_access(plot_id)
            
            # 如果没有抛出异常，说明验证成功
            actual_status = 200
            actual_message = "验证成功"
            
        except HTTPException as e:
            actual_status = e.status_code
            actual_message = e.detail
        except Exception as e:
            actual_status = 500
            actual_message = str(e)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 分析结果
        expected_status = test_case['expected_status']
        status_match = actual_status == expected_status
        message_match = test_case['expected_message'].lower() in actual_message.lower()
        test_passed = status_match and message_match
        
        return {
            "test_id": test_case['test_id'],
            "test_purpose": test_case['test_purpose'],
            "case_id": test_case['case_id'],
            "test_type": test_case['test_type'],
            "description": test_case.get('description', ''),
            "input_data": {
                "plotId": test_case.get('plotId'),
                "userId": test_case.get('userId'),
                "skip_auth": test_case.get('skip_auth', False)
            },
            "expected": {
                "status": expected_status,
                "message": test_case['expected_message']
            },
            "actual": {
                "status": actual_status,
                "message": actual_message,
                "execution_time": f"{execution_time:.4f}s"
            },
            "result": "PASS" if test_passed else "FAIL",
            "details": {
                "status_match": status_match,
                "message_match": message_match,
                "function_called": "validate_plot_access",
                "execution_method": "direct_function_call"
            }
        }
    
    async def run_validate_plot_access_tests_batch(self) -> List[Dict[str, Any]]:
        """
        批量运行所有预定义的validate_plot_access测试用例
        """
        test_cases = self.get_validate_plot_access_predefined_cases()
        return await self.run_validate_plot_access_tests(test_cases)
    
    def generate_test_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成测试报告
        """
        total_tests = len(results)
        passed_tests = len([r for r in results if r['result'] == 'PASS'])
        failed_tests = len([r for r in results if r['result'] == 'FAIL'])
        error_tests = len([r for r in results if r['result'] == 'ERROR'])
        
        # 按测试类型分组统计
        type_stats = {}
        for result in results:
            test_type = result['test_type']
            if test_type not in type_stats:
                type_stats[test_type] = {'total': 0, 'passed': 0, 'failed': 0, 'errors': 0}
            
            type_stats[test_type]['total'] += 1
            if result['result'] == 'PASS':
                type_stats[test_type]['passed'] += 1
            elif result['result'] == 'FAIL':
                type_stats[test_type]['failed'] += 1
            else:
                type_stats[test_type]['errors'] += 1
        
        # 计算平均执行时间
        execution_times = []
        for result in results:
            if 'execution_time' in result['actual']:
                time_str = result['actual']['execution_time'].replace('s', '')
                try:
                    execution_times.append(float(time_str))
                except:
                    pass
        
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        return {
            "summary": {
                "total": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "pass_rate": f"{(passed_tests/total_tests*100):.2f}%" if total_tests > 0 else "0%",
                "average_execution_time": f"{avg_execution_time:.4f}s"
            },
            "type_statistics": type_stats,
            "failed_cases": [r for r in results if r['result'] == 'FAIL'],
            "error_cases": [r for r in results if r['result'] == 'ERROR'],
            "function_info": self.get_function_source_code()
        }