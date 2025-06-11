## `GET /homework/code`
获取题目的初始代码
查询参数：
- problem: 题目名称 (triangle_judge, computer_selling, telecom_system, calendar_problem)

返回格式：
```json
{
    "success": true/false,
    "code": "代码字符串",
    "message": "提示信息"
}
```
## POST /homework/test
运行测试用例生成和执行
    
- 请求体格式（JSON）：
```json
    {
        "code": "要测试的代码字符串",
        "function_name": "函数名称",
        "test_method": "测试方法名称"
    }
```
- 返回格式：
```json
    {
        "success": true/false,
        "message": "信息",
        "function_name": "函数名称",
        "test_method": "测试方法",
        "test_name": "测试名称",
        "description": "测试描述",
        "summary": {
            "total_cases": 总用例数,
            "passed_cases": 通过用例数,
            "failed_cases": 失败用例数,
            "pass_rate": "通过率百分比"
        },
        "test_results": [
            {
                "ID": 用例ID,
                "Input": 输入参数,
                "Expected": 期望结果,
                "Actual": 实际结果,
                "Passed": true/false,
                "Duration": "执行时间"
            }
        ]
    }
```