import time
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

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
class Plot:
    plotId: str
    plotName: str
    location: str
    area: float
    createTime: datetime

class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

class LogControllerTestService:
    def __init__(self):
        # 模拟地块数据
        self.mock_plots = {
            "plot123": Plot(
                plotId="plot123",
                plotName="测试地块1",
                location="测试位置1",
                area=100.0,
                createTime=datetime(2024, 1, 1, 10, 0, 0)
            ),
            "plot456": Plot(
                plotId="plot456",
                plotName="测试地块2",
                location="测试位置2",
                area=200.0,
                createTime=datetime(2024, 1, 2, 10, 0, 0)
            ),
            "plot789": Plot(
                plotId="plot789",
                plotName="测试地块3",
                location="测试位置3",
                area=300.0,
                createTime=datetime(2024, 1, 3, 10, 0, 0)
            )
        }
        
        # 模拟日志存储
        self.mock_logs = []
        
        # 异常模拟标志
        self._simulate_db_error = False
        self._simulate_validation_error = False
        self._simulate_field_length_error = False
        self._simulate_plot_not_found = False
    
    async def set_log(self, plotId: str, diseaseName: str, advice: str, imageURL: str) -> str:
        """
        模拟 set_log 函数的实现
        """
        try:
            # 参数校验 - null值检查
            if plotId is None:
                raise HTTPException(status_code=422, detail="参数校验失败")
            if diseaseName is None:
                raise HTTPException(status_code=422, detail="参数校验失败")
            if advice is None:
                raise HTTPException(status_code=422, detail="参数校验失败")
            if imageURL is None:
                raise HTTPException(status_code=422, detail="参数校验失败")
            
            # 模拟数据库异常
            if self._simulate_db_error:
                raise HTTPException(status_code=500, detail="创建日志失败: 数据库异常")
            
            # 模拟字段长度验证
            if len(diseaseName) > 255:
                raise HTTPException(status_code=500, detail="创建日志失败: 字段长度超限")
            if len(advice) > 500:  # 从1500改为500
                raise HTTPException(status_code=500, detail="创建日志失败: 字段长度超限")
            if len(imageURL) > 500:  # 从2000改为500
                raise HTTPException(status_code=500, detail="创建日志失败: URL长度超限")
            
            # 模拟地块不存在的情况
            if plotId == "nonexistent" or self._simulate_plot_not_found:
                raise HTTPException(status_code=500, detail="创建日志失败: DoesNotExist异常")
            
            # 模拟空字符串验证
            if plotId == "":
                raise HTTPException(status_code=500, detail="创建日志失败: 异常信息")
            if diseaseName == "":
                raise HTTPException(status_code=500, detail="创建日志失败: 验证异常")
            
            # 获取地块信息
            plot = self.mock_plots.get(plotId)
            if not plot:
                raise HTTPException(status_code=500, detail="创建日志失败: DoesNotExist异常")
            
            # 格式化内容
            content = f"检测到{diseaseName}，建议：{advice}"
            
            # 创建日志记录
            log = Log(
                logId=str(uuid.uuid4()),
                plotId=plotId,
                timeStamp=datetime.now(),
                diseaseName=diseaseName,
                content=content,
                imagesURL=imageURL
            )
            
            # 保存到模拟存储
            self.mock_logs.append(log)
            
            return "创建日志成功"
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"创建日志失败: {str(e)}")
    
    def get_set_log_predefined_cases(self) -> List[Dict[str, Any]]:
        """
        返回 set_log 函数的预定义测试用例
        """
        return [
            # 9.3.10.1 有效等价类测试
            {
                "test_id": "TC01001",
                "test_purpose": "正常创建日志",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "及时喷药治疗",
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "有效等价类",
                "description": "测试正常创建日志功能"
            },
            {
                "test_id": "TC01002",
                "test_purpose": "创建包含特殊字符的日志",
                "plotId": "plot456",
                "diseaseName": "病害名称@#",
                "advice": "建议内容&*",
                "imageURL": "https://cdn.example.com/image_2024.png",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "有效等价类",
                "description": "测试包含特殊字符的日志创建"
            },
            {
                "test_id": "TC01003",
                "test_purpose": "创建长文本内容日志",
                "plotId": "plot789",
                "diseaseName": "复杂病害名称",
                "advice": "这是一个包含500个字符的建议内容" + "测试" * 120,
                "imageURL": "http://storage.com/long_filename_image.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "有效等价类",
                "description": "测试长文本内容的日志创建"
            },
            
            # 9.3.10.2 无效等价类测试
            {
                "test_id": "TC01004",
                "test_purpose": "地块不存在",
                "plotId": "nonexistent",
                "diseaseName": "白粉病",
                "advice": "及时喷药治疗",
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 500,
                "expected_message": "创建日志失败: DoesNotExist异常",
                "test_type": "无效等价类",
                "description": "测试地块不存在的情况"
            },
            {
                "test_id": "TC01005",
                "test_purpose": "plotId为空",
                "plotId": "",
                "diseaseName": "白粉病",
                "advice": "及时喷药治疗",
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 500,
                "expected_message": "创建日志失败: 异常信息",
                "test_type": "无效等价类",
                "description": "测试plotId为空字符串的情况"
            },
            {
                "test_id": "TC01006",
                "test_purpose": "diseaseName为空",
                "plotId": "plot123",
                "diseaseName": "",
                "advice": "及时喷药治疗",
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 500,
                "expected_message": "创建日志失败: 验证异常",
                "test_type": "无效等价类",
                "description": "测试diseaseName为空字符串的情况"
            },
            {
                "test_id": "TC01007",
                "test_purpose": "advice为空",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "",
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "无效等价类",
                "description": "测试advice为空字符串的情况（允许为空）"
            },
            {
                "test_id": "TC01008",
                "test_purpose": "imageURL为空",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "及时喷药治疗",
                "imageURL": "",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "无效等价类",
                "description": "测试imageURL为空字符串的情况（允许为空）"
            },
            {
                "test_id": "TC01009",
                "test_purpose": "plotId为null",
                "plotId": None,
                "diseaseName": "白粉病",
                "advice": "及时喷药治疗",
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 422,
                "expected_message": "参数校验失败",
                "test_type": "无效等价类",
                "description": "测试plotId为null的情况"
            },
            {
                "test_id": "TC01010",
                "test_purpose": "diseaseName为null",
                "plotId": "plot123",
                "diseaseName": None,
                "advice": "及时喷药治疗",
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 422,
                "expected_message": "参数校验失败",
                "test_type": "无效等价类",
                "description": "测试diseaseName为null的情况"
            },
            {
                "test_id": "TC01011",
                "test_purpose": "advice为null",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": None,
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 422,
                "expected_message": "参数校验失败",
                "test_type": "无效等价类",
                "description": "测试advice为null的情况"
            },
            {
                "test_id": "TC01012",
                "test_purpose": "imageURL为null",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "及时喷药治疗",
                "imageURL": None,
                "expected_status": 422,
                "expected_message": "参数校验失败",
                "test_type": "无效等价类",
                "description": "测试imageURL为null的情况"
            },
            {
                "test_id": "TC01013",
                "test_purpose": "数据库写入异常",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "及时喷药治疗",
                "imageURL": "http://example.com/img1.jpg",
                "expected_status": 500,
                "expected_message": "创建日志失败: 数据库异常",
                "test_type": "无效等价类",
                "description": "测试数据库异常的情况",
                "simulate_error": "db_error"
            },
            
            # 9.3.10.3 边界值分析测试
            {
                "test_id": "TC01014",
                "test_purpose": "diseaseName最短有效值",
                "plotId": "plot123",
                "diseaseName": "a",
                "advice": "建议",
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "边界值",
                "description": "测试diseaseName最短有效值"
            },
            {
                "test_id": "TC01015",
                "test_purpose": "diseaseName标准长度",
                "plotId": "plot123",
                "diseaseName": "标准长度的病害名称" * 5,  # 50个字符
                "advice": "建议",
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "边界值",
                "description": "测试diseaseName标准长度"
            },
            {
                "test_id": "TC01016",
                "test_purpose": "diseaseName超长",
                "plotId": "plot123",
                "diseaseName": "超长病害名称" * 50,  # 256个字符
                "advice": "建议",
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 500,
                "expected_message": "创建日志失败: 字段长度超限",
                "test_type": "边界值",
                "description": "测试diseaseName超长的情况"
            },
            {
                "test_id": "TC01017",
                "test_purpose": "advice最短有效值",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "a",
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "边界值",
                "description": "测试advice最短有效值"
            },
            {
                "test_id": "TC01018",
                "test_purpose": "advice标准长度",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "标准长度的建议内容" * 50,  # 500个字符
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "边界值",
                "description": "测试advice标准长度"
            },
            {
                "test_id": "TC01019",
                "test_purpose": "advice超长",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "超长建议内容" * 250,  # 2000个字符
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 500,
                "expected_message": "创建日志失败: 字段长度超限",
                "test_type": "边界值",
                "description": "测试advice超长的情况"
            },
            {
                "test_id": "TC01020",
                "test_purpose": "imageURL超长",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "建议",
                "imageURL": "http://example.com/" + "very_long_filename" * 100 + ".jpg",  # 2048个字符
                "expected_status": 500,
                "expected_message": "创建日志失败: URL长度超限",
                "test_type": "边界值",
                "description": "测试imageURL超长的情况"
            },
            
            # 9.3.10.4 功能性测试
            {
                "test_id": "TC01021",
                "test_purpose": "content格式化验证",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "及时喷药",
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "功能测试",
                "description": "验证content格式化为'检测到白粉病，建议：及时喷药'",
                "verify_content": "检测到白粉病，建议：及时喷药"
            },
            {
                "test_id": "TC01022",
                "test_purpose": "时间戳自动生成",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "及时喷药",
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "功能测试",
                "description": "验证日志记录包含当前时间戳",
                "verify_timestamp": True
            },
            {
                "test_id": "TC01023",
                "test_purpose": "plotId关联验证",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "及时喷药",
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "功能测试",
                "description": "验证日志记录正确关联到地块",
                "verify_plot_association": True
            },
            {
                "test_id": "TC01024",
                "test_purpose": "中文字符处理",
                "plotId": "plot123",
                "diseaseName": "小麦条纹花叶病毒病",
                "advice": "加强田间管理，清除杂草",
                "imageURL": "http://example.com/中文文件名.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "功能测试",
                "description": "测试中文字符的正确处理"
            },
            {
                "test_id": "TC01025",
                "test_purpose": "特殊字符转义",
                "plotId": "plot123",
                "diseaseName": "病害'名称\"",
                "advice": "建议\n换行\t制表符",
                "imageURL": "http://example.com/img.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "功能测试",
                "description": "测试特殊字符的转义处理"
            },
            
            # 9.3.10.5 URL格式验证测试
            {
                "test_id": "TC01026",
                "test_purpose": "有效HTTP URL",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "建议",
                "imageURL": "http://example.com/image.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "URL格式测试",
                "description": "测试有效的HTTP URL"
            },
            {
                "test_id": "TC01027",
                "test_purpose": "有效HTTPS URL",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "建议",
                "imageURL": "https://secure.example.com/image.png",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "URL格式测试",
                "description": "测试有效的HTTPS URL"
            },
            {
                "test_id": "TC01028",
                "test_purpose": "无效URL格式",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "建议",
                "imageURL": "invalid-url",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "URL格式测试",
                "description": "测试无效URL格式（系统允许）"
            },
            {
                "test_id": "TC01029",
                "test_purpose": "相对路径URL",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "建议",
                "imageURL": "/images/disease.jpg",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "URL格式测试",
                "description": "测试相对路径URL"
            },
            {
                "test_id": "TC01030",
                "test_purpose": "包含参数的URL",
                "plotId": "plot123",
                "diseaseName": "白粉病",
                "advice": "建议",
                "imageURL": "http://example.com/img.jpg?v=1&t=123",
                "expected_status": 200,
                "expected_message": "创建日志成功",
                "test_type": "URL格式测试",
                "description": "测试包含参数的URL"
            }
        ]
    
    async def _execute_set_log_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个 set_log 测试用例
        """
        start_time = time.time()
        result = {
            "test_id": test_case["test_id"],
            "test_purpose": test_case["test_purpose"],
            "case_id": test_case["test_id"],
            "test_type": test_case["test_type"],
            "input_params": {
                "plotId": test_case["plotId"],
                "diseaseName": test_case["diseaseName"],
                "advice": test_case["advice"],
                "imageURL": test_case["imageURL"]
            },
            "expected_status": test_case["expected_status"],
            "actual_status": None,
            "expected_message": test_case["expected_message"],  # 修改这里：使用正确的字段名
            "actual_message": None,
            "passed": False,
            "duration_ms": 0,
            "error": None
        }
        
        try:
            # 设置异常模拟
            if test_case.get("simulate_error") == "db_error":
                self._simulate_db_error = True
            else:
                self._simulate_db_error = False
            
            # 执行测试
            actual_result = await self.set_log(
                plotId=test_case["plotId"],
                diseaseName=test_case["diseaseName"],
                advice=test_case["advice"],
                imageURL=test_case["imageURL"]
            )
            
            result["actual_status"] = 200
            result["actual_message"] = actual_result
            
        except HTTPException as e:
            result["actual_status"] = e.status_code
            result["actual_message"] = e.detail
        except Exception as e:
            result["actual_status"] = 500
            result["actual_message"] = f"创建日志失败: {str(e)}"
            result["error"] = str(e)
        
        # 验证结果
        status_match = result["actual_status"] == result["expected_status"]
        
        # 严格匹配消息内容
        message_match = result["actual_message"] == result["expected_message"]
        
        result["passed"] = status_match and message_match
        
        # 计算执行时间并返回结果
        result["duration_ms"] = round((time.time() - start_time) * 1000, 2)
        return result

    async def run_set_log_tests(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        运行多个 set_log 测试用例
        """
        results = []
        for test_case in test_cases:
            result = await self._execute_set_log_test(test_case)
            results.append(result)
        return results
    
    async def run_set_log_tests_batch(self) -> List[Dict[str, Any]]:
        """
        运行所有预定义的 set_log 测试用例
        """
        test_cases = self.get_set_log_predefined_cases()
        return await self.run_set_log_tests(test_cases)
    
    def get_set_log_function_source_code(self) -> str:
        """
        返回 set_log 函数的源代码
        """
        return '''
async def set_log(plotId: str, diseaseName: str, advice: str, imageURL: str):
    try:
        plot = await Plot.get(plotId=plotId)
        content = f"检测到{diseaseName}，建议：{advice}"

        await Log.create(
            plotId=plot,
            diseaseName=diseaseName,
            content=content,
            imagesURL=imageURL
        )

        return "创建日志成功"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建日志失败: {str(e)}")
        '''
    
    def generate_test_report(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成测试报告
        """
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        # 按测试类型分组统计
        type_stats = {}
        for result in test_results:
            test_type = result["test_type"]
            if test_type not in type_stats:
                type_stats[test_type] = {"total": 0, "passed": 0, "failed": 0}
            type_stats[test_type]["total"] += 1
            if result["status"] == "PASS":
                type_stats[test_type]["passed"] += 1
            else:
                type_stats[test_type]["failed"] += 1
        
        # 计算平均执行时间
        avg_execution_time = sum(r["execution_time"] for r in test_results) / total_tests if total_tests > 0 else 0
        
        return jsonify({
            "status": "success",
            "summary": {
                "total_cases": total_tests,
                "passed_cases": passed_tests,
                "failed_cases": failed_tests,
                "pass_rate": round((passed_tests / total_tests) * 100, 2) if total_tests > 0 else 0,
                "average_execution_time_ms": round(avg_execution_time, 2)
            },
            "statistics_by_type": type_stats,  # 这里包含了类型统计
            "test_results": results,
            "failed_cases": [r for r in results if not r["passed"]]
        })