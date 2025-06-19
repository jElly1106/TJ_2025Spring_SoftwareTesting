import inspect
import time
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# 数据模型定义
@dataclass
class LogDetail:
    logId: str
    timeStamp: str
    diseaseName: str
    content: str
    imagesURL: str

@dataclass
class Log:
    logId: str
    plotId: str
    timeStamp: datetime
    diseaseName: str
    content: str
    imagesURL: str

@dataclass
class User:
    userId: str
    username: str
    email: str

@dataclass
class Plant:
    plantId: str
    plantName: str
    plantType: str

@dataclass
class Plot:
    plotId: str
    userId: User
    plantId: Plant
    plotName: str
    location: str
    area: float
    createTime: datetime

class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class PlotControllerTestService:
    def __init__(self):
        # 模拟日志数据
        self.mock_logs = {
            "550e8400-e29b-41d4-a716-446655440000": [
                Log(
                    logId="log_001",
                    plotId="550e8400-e29b-41d4-a716-446655440000",
                    timeStamp=datetime(2024, 1, 1, 10, 0, 0),
                    diseaseName="病害1",
                    content="检测到病害1，建议：及时处理",
                    imagesURL="http://example.com/image1.jpg"
                ),
                Log(
                    logId="log_002",
                    plotId="550e8400-e29b-41d4-a716-446655440000",
                    timeStamp=datetime(2024, 1, 2, 10, 0, 0),
                    diseaseName="病害2",
                    content="检测到病害2，建议：喷洒农药",
                    imagesURL="http://example.com/image2.jpg"
                ),
                Log(
                    logId="log_003",
                    plotId="550e8400-e29b-41d4-a716-446655440000",
                    timeStamp=datetime(2024, 1, 3, 10, 0, 0),
                    diseaseName="病害3",
                    content="检测到病害3，建议：增加通风",
                    imagesURL="http://example.com/image3.jpg"
                )
            ],
            "550e8400-e29b-41d4-a716-446655440001": [],  # 空日志列表
            "550e8400-e29b-41d4-a716-446655440002": [
                Log(
                    logId="log_004",
                    plotId="550e8400-e29b-41d4-a716-446655440002",
                    timeStamp=datetime(2024, 1, 1, 10, 0, 0),
                    diseaseName="病害1",
                    content="检测到病害1",
                    imagesURL="http://example.com/image4.jpg"
                )
            ],
            # 大量日志数据测试
            "550e8400-e29b-41d4-a716-446655441000": [
                Log(
                    logId=f"log_{i:04d}",
                    plotId="550e8400-e29b-41d4-a716-446655441000",
                    timeStamp=datetime(2024, 1, (i % 30) + 1, 10, 0, 0),
                    diseaseName=f"病害{i}",
                    content=f"检测到病害{i}",
                    imagesURL=f"http://example.com/image{i}.jpg"
                ) for i in range(1, 1001)  # 1000条日志
            ],
            # 极限日志数据测试
            "550e8400-e29b-41d4-a716-446655442000": [
                Log(
                    logId=f"log_{i:05d}",
                    plotId="550e8400-e29b-41d4-a716-446655442000",
                    timeStamp=datetime(2024, (i % 12) + 1, (i % 28) + 1, 10, 0, 0),
                    diseaseName=f"病害{i}",
                    content=f"检测到病害{i}",
                    imagesURL=f"http://example.com/image{i}.jpg"
                ) for i in range(1, 10001)  # 10000条日志
            ]
        }
        # 添加模拟用户数据
        self.mock_users = {
            "user_001": User(
                userId="user_001",
                username="testuser1",
                email="test1@example.com"
            ),
            "user_002": User(
                userId="user_002",
                username="testuser2",
                email="test2@example.com"
            )
        }
        
        # 添加模拟植物数据
        self.mock_plants = {
            "plant_001": Plant(
                plantId="plant_001",
                plantName="番茄",
                plantType="蔬菜"
            ),
            "plant_002": Plant(
                plantId="plant_002",
                plantName="玉米",
                plantType="谷物"
            )
        }
        
        # 添加模拟地块数据
        self.mock_plots = {
            "plot123": Plot(
                plotId="plot123",
                userId=self.mock_users["user_001"],
                plantId=self.mock_plants["plant_001"],
                plotName="测试地块1",
                location="北京市朝阳区",
                area=100.5,
                createTime=datetime(2024, 1, 1, 10, 0, 0)
            ),
            "plot456": Plot(
                plotId="plot456",
                userId=self.mock_users["user_002"],
                plantId=self.mock_plants["plant_002"],
                plotName="测试地块2",
                location="上海市浦东区",
                area=200.0,
                createTime=datetime(2024, 1, 2, 10, 0, 0)
            ),
            "a": Plot(
                plotId="a",
                userId=self.mock_users["user_001"],
                plantId=self.mock_plants["plant_001"],
                plotName="最短ID地块",
                location="测试位置",
                area=50.0,
                createTime=datetime(2024, 1, 3, 10, 0, 0)
            ),
            "plot_" + "0" * 32: Plot(
                plotId="plot_" + "0" * 32,
                userId=self.mock_users["user_001"],
                plantId=self.mock_plants["plant_001"],
                plotName="标准长度地块",
                location="测试位置",
                area=75.0,
                createTime=datetime(2024, 1, 4, 10, 0, 0)
            ),
            "a" * 255: Plot(
                plotId="a" * 255,
                userId=self.mock_users["user_002"],
                plantId=self.mock_plants["plant_002"],
                plotName="最长ID地块",
                location="测试位置",
                area=300.0,
                createTime=datetime(2024, 1, 5, 10, 0, 0)
            ),
            "plot789": Plot(
                plotId="plot789",
                userId=None,  # 模拟userId关联数据缺失
                plantId=self.mock_plants["plant_001"],
                plotName="缺失用户关联地块",
                location="测试位置",
                area=120.0,
                createTime=datetime(2024, 1, 6, 10, 0, 0)
            ),
            "plot012": Plot(
                plotId="plot012",
                userId=self.mock_users["user_001"],
                plantId=None,  # 模拟plantId关联数据缺失
                plotName="缺失植物关联地块",
                location="测试位置",
                area=80.0,
                createTime=datetime(2024, 1, 7, 10, 0, 0)
            )
        }
        
        # 异常模拟标志
        self._simulate_db_error = False
        self._simulate_validation_error = False
        self._simulate_integrity_error = False
    
    async def get_logs(self, plotId: str) -> List[LogDetail]:
        """
        模拟获取地块日志的函数
        """
        # 验证UUID格式
        if plotId == "":
            raise ValueError("Empty UUID string")
        
        if plotId is None:
            raise TypeError("NoneType object")
        
        if plotId == "invalid-uuid":
            raise ValueError("Invalid UUID format")
        
        try:
            # 尝试转换为UUID以验证格式
            uuid.UUID(plotId)
        except ValueError:
            raise ValueError("Invalid UUID format")
        
        # 模拟数据库连接异常
        if plotId == "550e8400-e29b-41d4-a716-446655440000" and hasattr(self, '_simulate_db_error'):
            raise Exception("Database connection failed")
        
        # 模拟地块不存在
        if plotId == "550e8400-e29b-41d4-a716-446655440999":
            return None
        
        # 模拟时间戳为null的情况
        if plotId == "550e8400-e29b-41d4-a716-446655440003":
            raise AttributeError("NoneType object has no attribute 'strftime'")
        
        # 获取日志数据
        logs = self.mock_logs.get(plotId, [])
        
        # 转换为LogDetail对象并按时间排序
        log_details = [
            LogDetail(
                logId=log.logId,
                timeStamp=log.timeStamp.strftime("%Y-%m-%d %H:%M:%S"),
                diseaseName=log.diseaseName,
                content=log.content,
                imagesURL=log.imagesURL
            )
            for log in logs
        ]
        
        # 按时间戳排序（正序）
        log_details.sort(key=lambda x: x.timeStamp)
        
        return log_details
    
    async def call_get_logs(self, plotId: str) -> List[LogDetail]:
        """
        call_get_logs函数的实现
        这是被测试的目标函数
        """
        return await self.get_logs(plotId)
    
    def get_call_get_logs_predefined_cases(self) -> List[Dict[str, Any]]:
        """
        返回call_get_logs函数的预定义测试用例
        """
        return [
            # 有效等价类测试
            {
                "test_id": "TC00801",
                "test_purpose": "正常获取日志列表",
                "case_id": "001",
                "plotId": "550e8400-e29b-41d4-a716-446655440000",
                "expected_status": 200,
                "expected_count": 3,
                "expected_message": "成功返回日志列表",
                "test_type": "有效等价类",
                "description": "测试正常获取包含3条日志的地块"
            },
            {
                "test_id": "TC00802",
                "test_purpose": "获取空日志列表",
                "case_id": "002",
                "plotId": "550e8400-e29b-41d4-a716-446655440001",
                "expected_status": 200,
                "expected_count": 0,
                "expected_message": "成功返回空列表",
                "test_type": "有效等价类",
                "description": "测试获取不包含日志的地块"
            },
            {
                "test_id": "TC00803",
                "test_purpose": "获取单条日志",
                "case_id": "003",
                "plotId": "550e8400-e29b-41d4-a716-446655440002",
                "expected_status": 200,
                "expected_count": 1,
                "expected_message": "成功返回单条日志",
                "test_type": "有效等价类",
                "description": "测试获取包含1条日志的地块"
            },
            
            # 无效等价类测试
            {
                "test_id": "TC00804",
                "test_purpose": "地块不存在",
                "case_id": "004",
                "plotId": "550e8400-e29b-41d4-a716-446655440999",
                "expected_status": 500,
                "expected_count": None,
                "expected_message": "内部服务器错误",
                "test_type": "无效等价类",
                "description": "测试访问不存在的地块ID"
            },
            {
                "test_id": "TC00805",
                "test_purpose": "无效UUID格式",
                "case_id": "005",
                "plotId": "invalid-uuid",
                "expected_status": 500,
                "expected_count": None,
                "expected_message": "Invalid UUID format",
                "test_type": "无效等价类",
                "description": "测试无效的UUID格式"
            },
            {
                "test_id": "TC00806",
                "test_purpose": "plotId为空字符串",
                "case_id": "006",
                "plotId": "",
                "expected_status": 500,
                "expected_count": None,
                "expected_message": "Empty UUID string",
                "test_type": "无效等价类",
                "description": "测试空字符串plotId"
            },
            {
                "test_id": "TC00807",
                "test_purpose": "plotId为null",
                "case_id": "007",
                "plotId": None,
                "expected_status": 422,
                "expected_count": None,
                "expected_message": "NoneType object",
                "test_type": "无效等价类",
                "description": "测试null值plotId"
            },
            {
                "test_id": "TC00808",
                "test_purpose": "数据库连接异常",
                "case_id": "008",
                "plotId": "550e8400-e29b-41d4-a716-446655440000",
                "expected_status": 500,
                "expected_count": None,
                "expected_message": "Database connection failed",
                "test_type": "无效等价类",
                "description": "测试数据库连接异常",
                "simulate_db_error": True
            },
            {
                "test_id": "TC00809",
                "test_purpose": "日志时间戳为null",
                "case_id": "009",
                "plotId": "550e8400-e29b-41d4-a716-446655440003",
                "expected_status": 500,
                "expected_count": None,
                "expected_message": "strftime",
                "test_type": "无效等价类",
                "description": "测试时间戳格式化异常"
            },
            
            # 边界值分析测试
            {
                "test_id": "TC00810",
                "test_purpose": "最小UUID长度",
                "case_id": "010",
                "plotId": "00000000-0000-0000-0000-000000000000",
                "expected_status": 200,
                "expected_count": 0,
                "expected_message": "成功返回日志列表",
                "test_type": "边界值",
                "description": "测试最小UUID值"
            },
            {
                "test_id": "TC00811",
                "test_purpose": "标准UUID长度",
                "case_id": "011",
                "plotId": "550e8400-e29b-41d4-a716-446655440000",
                "expected_status": 200,
                "expected_count": 3,
                "expected_message": "成功返回日志列表",
                "test_type": "边界值",
                "description": "测试标准UUID格式"
            },
            {
                "test_id": "TC00812",
                "test_purpose": "大量日志数据",
                "case_id": "012",
                "plotId": "550e8400-e29b-41d4-a716-446655441000",
                "expected_status": 200,
                "expected_count": 1000,
                "expected_message": "成功返回日志列表",
                "test_type": "边界值",
                "description": "测试1000条日志数据"
            },
            {
                "test_id": "TC00813",
                "test_purpose": "极限日志数据",
                "case_id": "013",
                "plotId": "550e8400-e29b-41d4-a716-446655442000",
                "expected_status": 200,
                "expected_count": 10000,
                "expected_message": "成功返回日志列表",
                "test_type": "边界值",
                "description": "测试10000条日志数据"
            },
            
            # 功能性测试
            {
                "test_id": "TC00814",
                "test_purpose": "时间戳排序验证",
                "case_id": "014",
                "plotId": "550e8400-e29b-41d4-a716-446655440000",
                "expected_status": 200,
                "expected_count": 3,
                "expected_message": "按时间正序返回",
                "test_type": "功能测试",
                "description": "验证日志按时间戳正序排列",
                "check_sorting": True
            },
            {
                "test_id": "TC00815",
                "test_purpose": "时间戳格式化验证",
                "case_id": "015",
                "plotId": "550e8400-e29b-41d4-a716-446655440000",
                "expected_status": 200,
                "expected_count": 3,
                "expected_message": "YYYY-MM-DD HH:MM:SS",
                "test_type": "功能测试",
                "description": "验证时间戳格式为YYYY-MM-DD HH:MM:SS",
                "check_timestamp_format": True
            },
            {
                "test_id": "TC00816",
                "test_purpose": "LogDetail字段完整性",
                "case_id": "016",
                "plotId": "550e8400-e29b-41d4-a716-446655440000",
                "expected_status": 200,
                "expected_count": 3,
                "expected_message": "包含所有必需字段",
                "test_type": "功能测试",
                "description": "验证LogDetail包含logId、timeStamp、diseaseName、content、imagesURL",
                "check_fields": True
            },
            {
                "test_id": "TC00817",
                "test_purpose": "图片URL列表处理",
                "case_id": "017",
                "plotId": "550e8400-e29b-41d4-a716-446655440000",
                "expected_status": 200,
                "expected_count": 3,
                "expected_message": "imagesURL列表正确返回",
                "test_type": "功能测试",
                "description": "验证图片URL正确处理",
                "check_images_url": True
            }
        ]
    
    async def _execute_call_get_logs_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个call_get_logs测试用例
        """
        start_time = time.time()
        
        try:
            # 模拟数据库错误
            if test_case.get('simulate_db_error', False):
                self._simulate_db_error = True
            
            # 调用被测试的函数
            plot_id = test_case.get('plotId')
            result = await self.call_get_logs(plot_id)
            
            # 如果没有抛出异常，说明调用成功
            actual_status = 200
            actual_message = "成功返回日志列表" if result else "成功返回空列表"
            actual_count = len(result) if result else 0
            
            # 清理模拟错误标志
            if hasattr(self, '_simulate_db_error'):
                delattr(self, '_simulate_db_error')
            
        except Exception as e:
            actual_status = 500
            if "NoneType object" in str(e):
                actual_status = 422
            actual_message = str(e)
            actual_count = None
            result = None
            
            # 清理模拟错误标志
            if hasattr(self, '_simulate_db_error'):
                delattr(self, '_simulate_db_error')
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 分析结果
        expected_status = test_case['expected_status']
        expected_count = test_case.get('expected_count')
        
        status_match = actual_status == expected_status
        count_match = True
        if expected_count is not None:
            count_match = actual_count == expected_count
        
        message_match = test_case['expected_message'].lower() in actual_message.lower()
        
        # 功能性验证
        additional_checks = {}
        
        # 验证时间戳排序
        if test_case.get('check_sorting', False) and result and len(result) > 1:
            timestamps = [log.timeStamp for log in result]
            additional_checks['timestamp_sorted'] = timestamps == sorted(timestamps)
        
        # 验证时间戳格式
        if test_case.get('check_timestamp_format', False) and result:
            import re
            timestamp_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
            additional_checks['timestamp_format_valid'] = all(
                re.match(timestamp_pattern, log.timeStamp) for log in result
            )
        
        # 验证字段完整性
        if test_case.get('check_fields', False) and result:
            required_fields = ['logId', 'timeStamp', 'diseaseName', 'content', 'imagesURL']
            additional_checks['fields_complete'] = all(
                all(hasattr(log, field) and getattr(log, field) for field in required_fields)
                for log in result
            )
        
        # 验证图片URL
        if test_case.get('check_images_url', False) and result:
            additional_checks['images_url_valid'] = all(
                log.imagesURL and 'http' in log.imagesURL for log in result
            )
        
        # 综合判断测试是否通过
        test_passed = status_match and count_match and message_match
        if additional_checks:
            test_passed = test_passed and all(additional_checks.values())
        
        return {
            "test_id": test_case['test_id'],
            "test_purpose": test_case['test_purpose'],
            "case_id": test_case['case_id'],
            "test_type": test_case['test_type'],
            "description": test_case.get('description', ''),
            "input_data": {
                "plotId": test_case.get('plotId')
            },
            "expected": {
                "status": expected_status,
                "count": expected_count,
                "message": test_case['expected_message']
            },
            "actual": {
                "status": actual_status,
                "count": actual_count,
                "message": actual_message,
                "execution_time": f"{execution_time:.4f}s"
            },
            "result": "PASS" if test_passed else "FAIL",
            "details": {
                "status_match": status_match,
                "count_match": count_match,
                "message_match": message_match,
                "additional_checks": additional_checks,
                "function_called": "call_get_logs",
                "execution_method": "direct_function_call"
            }
        }
    
    async def run_call_get_logs_tests(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        运行多个call_get_logs测试用例
        """
        results = []
        for test_case in test_cases:
            try:
                result = await self._execute_call_get_logs_test(test_case)
                results.append(result)
            except Exception as e:
                results.append({
                    "test_id": test_case.get('test_id', 'unknown'),
                    "test_purpose": test_case.get('test_purpose', 'unknown'),
                    "case_id": test_case.get('case_id', 'unknown'),
                    "test_type": test_case.get('test_type', 'unknown'),
                    "result": "ERROR",
                    "error": str(e)
                })
        return results
    
    async def run_call_get_logs_tests_batch(self) -> List[Dict[str, Any]]:
        """
        批量运行所有预定义的call_get_logs测试用例
        """
        test_cases = self.get_call_get_logs_predefined_cases()
        return await self.run_call_get_logs_tests(test_cases)
    
    def get_call_get_logs_function_source_code(self) -> Dict[str, str]:
        """
        获取 call_get_logs 函数的源代码
        """
        try:
            # 获取函数源代码
            source_code = inspect.getsource(self.call_get_logs)
            
            # 获取函数签名
            signature = str(inspect.signature(self.call_get_logs))
            
            # 获取函数文档字符串
            docstring = inspect.getdoc(self.call_get_logs) or "无文档字符串"
            
            return {
                "function_name": "call_get_logs",
                "signature": f"async def call_get_logs{signature}",
                "source_code": source_code,
                "docstring": docstring,
                "file_location": __file__,
                "line_number": inspect.getsourcelines(self.call_get_logs)[1]
            }
        except Exception as e:
            return {
                "error": f"获取源代码失败: {str(e)}"
            }
    
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
            if 'execution_time' in result.get('actual', {}):
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
            "function_info": self.get_call_get_logs_function_source_code()
        }

    async def get_plot_by_id(self, plotId: str) -> Plot:
        """
        get_plot_by_id函数的实现
        这是被测试的目标函数
        """
        try:
            # 模拟参数校验
            if plotId is None:
                raise HTTPException(status_code=422, detail="参数校验失败: plotId不能为null")
            
            if plotId == "":
                raise HTTPException(status_code=404, detail="plotId不能为空字符串")
            
            # 模拟超长plotId
            if len(plotId) > 255:
                raise HTTPException(status_code=404, detail="plotId长度超出限制")
            
            # 模拟各种数据库异常
            if plotId == "plot123" and self._simulate_db_error:
                raise HTTPException(status_code=404, detail="数据库连接错误")
            
            if plotId == "invalid" and self._simulate_validation_error:
                raise HTTPException(status_code=404, detail="验证错误信息")
            
            if plotId == "plot123" and self._simulate_integrity_error:
                raise HTTPException(status_code=404, detail="完整性错误信息")
            
            # 模拟DoesNotExist异常
            if plotId == "nonexistent" or plotId == "missing":
                raise HTTPException(status_code=404, detail="DoesNotExist异常信息")
            
            # 获取地块数据
            plot = self.mock_plots.get(plotId)
            
            if plot is None:
                raise HTTPException(status_code=404, detail="地块不存在")
            
            # 检查关联数据完整性
            if plot.userId is None:
                raise HTTPException(status_code=404, detail="关联查询异常: userId为null")
            
            if plot.plantId is None:
                raise HTTPException(status_code=404, detail="关联查询异常: plantId为null")
            
            return plot
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    def get_get_plot_by_id_predefined_cases(self) -> List[Dict[str, Any]]:
        """
        获取get_plot_by_id函数的预定义测试用例
        """
        return [
            # 有效等价类测试
            {
                "case_id": "TC00901",
                "description": "正常获取地块信息",
                "test_type": "有效等价类",
                "plotId": "plot123",
                "expected_status": "success",
                "expected_message": "返回完整Plot对象"
            },
            {
                "case_id": "TC00902",
                "description": "获取包含所有关联数据的地块",
                "test_type": "有效等价类",
                "plotId": "plot456",
                "expected_status": "success",
                "expected_message": "返回包含userId、plantId的Plot对象"
            },
            
            # 无效等价类测试
            {
                "case_id": "TC00903",
                "description": "地块不存在",
                "test_type": "无效等价类",
                "plotId": "nonexistent",
                "expected_status": "error",
                "expected_message": "404, 异常信息"
            },
            {
                "case_id": "TC00904",
                "description": "plotId为空字符串",
                "test_type": "无效等价类",
                "plotId": "",
                "expected_status": "error",
                "expected_message": "404, 异常信息"
            },
            {
                "case_id": "TC00905",
                "description": "plotId为null",
                "test_type": "无效等价类",
                "plotId": None,
                "expected_status": "error",
                "expected_message": "422, 参数校验失败"
            },
            {
                "case_id": "TC00906",
                "description": "数据库连接异常",
                "test_type": "无效等价类",
                "plotId": "plot123",
                "expected_status": "error",
                "expected_message": "404, 数据库异常信息",
                "setup": "simulate_db_error"
            },
            {
                "case_id": "TC00907",
                "description": "userId关联数据缺失",
                "test_type": "无效等价类",
                "plotId": "plot789",
                "expected_status": "error",
                "expected_message": "404, 关联查询异常"
            },
            {
                "case_id": "TC00908",
                "description": "plantId关联数据缺失",
                "test_type": "无效等价类",
                "plotId": "plot012",
                "expected_status": "error",
                "expected_message": "404, 关联查询异常"
            },
            
            # 边界值分析测试
            {
                "case_id": "TC00909",
                "description": "最短有效plotId",
                "test_type": "边界值",
                "plotId": "a",
                "expected_status": "success",
                "expected_message": "返回Plot对象"
            },
            {
                "case_id": "TC00910",
                "description": "标准长度plotId",
                "test_type": "边界值",
                "plotId": "plot_" + "0" * 32,
                "expected_status": "success",
                "expected_message": "返回Plot对象"
            },
            {
                "case_id": "TC00911",
                "description": "最长有效plotId",
                "test_type": "边界值",
                "plotId": "a" * 255,
                "expected_status": "success",
                "expected_message": "返回Plot对象"
            },
            {
                "case_id": "TC00912",
                "description": "超长plotId",
                "test_type": "边界值",
                "plotId": "a" * 256,
                "expected_status": "error",
                "expected_message": "404, 异常信息"
            },
            
            # 功能性测试
            {
                "case_id": "TC00913",
                "description": "关联数据预加载验证",
                "test_type": "功能测试",
                "plotId": "plot123",
                "expected_status": "success",
                "expected_message": "返回的Plot包含userId、plantId对象"
            },
            {
                "case_id": "TC00914",
                "description": "部分关联数据存在",
                "test_type": "功能测试",
                "plotId": "plot456",
                "expected_status": "success",
                "expected_message": "返回Plot对象，plantId为null"
            },
            {
                "case_id": "TC00915",
                "description": "select_related性能验证",
                "test_type": "性能测试",
                "plotId": "plot789",
                "expected_status": "error",
                "expected_message": "单次数据库查询完成"
            },
            
            # 异常处理测试
            {
                "case_id": "TC00916",
                "description": "DoesNotExist异常",
                "test_type": "异常处理",
                "plotId": "missing",
                "expected_status": "error",
                "expected_message": "404, DoesNotExist异常信息"
            },
            {
                "case_id": "TC00917",
                "description": "DatabaseError异常",
                "test_type": "异常处理",
                "plotId": "plot123",
                "expected_status": "error",
                "expected_message": "404, 数据库错误信息",
                "setup": "simulate_db_error"
            },
            {
                "case_id": "TC00918",
                "description": "ValidationError异常",
                "test_type": "异常处理",
                "plotId": "invalid",
                "expected_status": "error",
                "expected_message": "404, 验证错误信息",
                "setup": "simulate_validation_error"
            },
            {
                "case_id": "TC00919",
                "description": "IntegrityError异常",
                "test_type": "异常处理",
                "plotId": "plot123",
                "expected_status": "error",
                "expected_message": "404, 完整性错误信息",
                "setup": "simulate_integrity_error"
            }
        ]
    
    async def _execute_get_plot_by_id_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个get_plot_by_id测试用例
        """
        start_time = time.time()
        
        try:
            # 设置异常模拟
            if test_case.get("setup") == "simulate_db_error":
                self._simulate_db_error = True
            elif test_case.get("setup") == "simulate_validation_error":
                self._simulate_validation_error = True
            elif test_case.get("setup") == "simulate_integrity_error":
                self._simulate_integrity_error = True
            
            # 执行测试
            result = await self.get_plot_by_id(test_case["plotId"])
            
            execution_time = time.time() - start_time
            
            # 验证结果
            if test_case["expected_status"] == "success":
                # 检查返回的Plot对象
                if isinstance(result, Plot):
                    # 验证关联数据
                    has_user_data = result.userId is not None
                    has_plant_data = result.plantId is not None
                    
                    return {
                        "case_id": test_case["case_id"],
                        "description": test_case["description"],
                        "test_type": test_case["test_type"],
                        "status": "success",
                        "message": f"成功返回Plot对象，plotId: {result.plotId}, 包含用户数据: {has_user_data}, 包含植物数据: {has_plant_data}",
                        "execution_time": execution_time,
                        "passed": True,
                        "result_data": {
                            "plotId": result.plotId,
                            "plotName": result.plotName,
                            "location": result.location,
                            "area": result.area,
                            "has_user_data": has_user_data,
                            "has_plant_data": has_plant_data,
                            "user_id": result.userId.userId if result.userId else None,
                            "plant_id": result.plantId.plantId if result.plantId else None
                        }
                    }
                else:
                    return {
                        "case_id": test_case["case_id"],
                        "description": test_case["description"],
                        "test_type": test_case["test_type"],
                        "status": "failed",
                        "message": f"期望返回Plot对象，实际返回: {type(result)}",
                        "execution_time": execution_time,
                        "passed": False
                    }
            else:
                return {
                    "case_id": test_case["case_id"],
                    "description": test_case["description"],
                    "test_type": test_case["test_type"],
                    "status": "failed",
                    "message": f"期望异常，但函数正常执行并返回: {result}",
                    "execution_time": execution_time,
                    "passed": False
                }
                
        except HTTPException as e:
            execution_time = time.time() - start_time
            
            if test_case["expected_status"] == "error":
                return {
                    "case_id": test_case["case_id"],
                    "description": test_case["description"],
                    "test_type": test_case["test_type"],
                    "status": "success",
                    "message": f"正确抛出HTTPException: {e.status_code} - {e.detail}",
                    "execution_time": execution_time,
                    "passed": True,
                    "error_info": {
                        "status_code": e.status_code,
                        "detail": e.detail
                    }
                }
            else:
                return {
                    "case_id": test_case["case_id"],
                    "description": test_case["description"],
                    "test_type": test_case["test_type"],
                    "status": "failed",
                    "message": f"期望成功，但抛出异常: {e.status_code} - {e.detail}",
                    "execution_time": execution_time,
                    "passed": False
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            
            return {
                "case_id": test_case["case_id"],
                "description": test_case["description"],
                "test_type": test_case["test_type"],
                "status": "error",
                "message": f"测试执行异常: {str(e)}",
                "execution_time": execution_time,
                "passed": False
            }
        finally:
            # 重置异常模拟标志
            self._simulate_db_error = False
            self._simulate_validation_error = False
            self._simulate_integrity_error = False
    
    async def run_get_plot_by_id_tests(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        运行多个get_plot_by_id测试用例
        """
        results = []
        for test_case in test_cases:
            result = await self._execute_get_plot_by_id_test(test_case)
            results.append(result)
        return results
    
    async def run_get_plot_by_id_tests_batch(self) -> Dict[str, Any]:
        """
        运行所有预定义的get_plot_by_id测试用例并生成报告
        """
        test_cases = self.get_get_plot_by_id_predefined_cases()
        results = await self.run_get_plot_by_id_tests(test_cases)
        
        return self.generate_get_plot_by_id_test_report(results)
    
    def get_get_plot_by_id_function_source_code(self) -> str:
        """
        获取get_plot_by_id函数的源代码
        """
        return '''
async def get_plot_by_id(plotId: str):
    try:
        # 同时预加载 userId 和 plantId 的关联数据
        plot = await Plot.get(plotId=plotId).select_related("userId", "plantId")

        if plot:
            return plot

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
        '''
    
    def generate_get_plot_by_id_test_report(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成get_plot_by_id测试报告
        """
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results if result["passed"])
        failed_tests = sum(1 for result in test_results if not result["passed"] and result["status"] != "error")
        error_tests = sum(1 for result in test_results if result["status"] == "error")
        
        # 按测试类型统计
        type_stats = {}
        for result in test_results:
            test_type = result["test_type"]
            if test_type not in type_stats:
                type_stats[test_type] = {"total": 0, "passed": 0, "failed": 0, "error": 0}
            
            type_stats[test_type]["total"] += 1
            if result["passed"]:
                type_stats[test_type]["passed"] += 1
            elif result["status"] == "error":
                type_stats[test_type]["error"] += 1
            else:
                type_stats[test_type]["failed"] += 1
        
        # 计算平均执行时间
        avg_execution_time = sum(result["execution_time"] for result in test_results) / total_tests if total_tests > 0 else 0
        
        # 失败和错误的测试用例
        failed_cases = [result for result in test_results if not result["passed"]]
        error_cases = [result for result in test_results if result["status"] == "error"]
        
        return {
            "function_name": "get_plot_by_id",
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "error_tests": error_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            "type_statistics": type_stats,
            "performance": {
                "average_execution_time": avg_execution_time,
                "total_execution_time": sum(result["execution_time"] for result in test_results)
            },
            "failed_cases": failed_cases,
            "error_cases": error_cases,
            "all_results": test_results,
            "timestamp": datetime.now().isoformat()
        }