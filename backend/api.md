## `GET /homework/code`
获取题目的初始代码
查询参数：
- problem: 题目名称 (triangle_judge, computer_selling, telecom_system, calendar_problem, seller_bonus)

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

## 各函数支持的测试方法:
triangle_judge:
  1. boundary_basic - 基本边界值测试
  2. boundary_robust - 健壮边界值测试
  3. equivalent_weak - 弱一般等价类测试
  4. equivalent_strong - 强一般等价类测试
  5. equivalent_weak_robust - 弱健壮等价类测试
  6. equivalent_strong_robust - 强健壮等价类测试

computer_selling:
  1. boundary_basic - 基本边界值测试
  2. boundary_robust - 健壮边界值测试

telecom_system:
  1. boundary_basic - 基本边界值测试
  2. boundary_robust - 健壮边界值测试
  3. equivalent_weak - 弱一般等价类测试
  4. equivalent_strong - 强一般等价类测试
  5. equivalent_weak_robust - 弱健壮等价类测试
  6. equivalent_strong_robust - 强健壮等价类测试
  7. decision_table - 决策表测试

calendar_problem:
    1. boundary_basic - 基本边界值测试
    2. boundary_robust - 健壮边界值测试
    3. equivalent_weak - 弱一般等价类测试
    4. equivalent_strong - 强一般等价类测试
    5. equivalent_weak_robust - 弱健壮等价类测试
    6. equivalent_strong_robust - 强健壮等价类测试
    7. decision_table - 决策表测试

seller_bonus:

1.statement_coverage: 语句覆盖

2.judgement_coverage: 判断覆盖

3.condition_coverage: 条件覆盖

4.judgement_condition_coverage: 判断—条件覆盖

5.condition_combination_coverage: 条件组合覆盖



```Json
GET /scan_classes
```

请求参数：

directory：项目根路径,如 D:/P-guard/backend

响应示例

```json
{

  "data": {

​    "database.redis_config.RedisConfig": {}, // 类名

​    "models.models.City": {

​      "clone": [ // 方法名：[方法参数]

​        { 

​          "annotation": "Any", // 参数类型注解

​          "default": "<object object at 0x00000293491D6C50>", // 参数默认值

​          "kind": "POSITIONAL_OR_KEYWORD", // 参数类型（位置传递或关键字传递）

​          "name": "pk"  //参数名

​        }

​      ],

​      "delete": [

​        {

​          "annotation": "BaseDBAsyncClient | None",

​          "default": "None",

​          "kind": "POSITIONAL_OR_KEYWORD",

​          "name": "using_db"

​        }

​      ],

​      "fetch_related": [

​        {

​          "annotation": "Any",

​          "default": null,

​          "kind": "VAR_POSITIONAL",

​          "name": "args"

​        },

​        {

​          "annotation": "BaseDBAsyncClient | None",

​          "default": "None",

​          "kind": "KEYWORD_ONLY",

​          "name": "using_db"

​        }

​      ],

​      "refresh_from_db": [

​        {

​          "annotation": "Iterable[str] | None",

​          "default": "None",

​          "kind": "POSITIONAL_OR_KEYWORD",

​          "name": "fields"

​        },

​        {

​          "annotation": "BaseDBAsyncClient | None",

​          "default": "None",

​          "kind": "POSITIONAL_OR_KEYWORD",

​          "name": "using_db"

​        }

​      ],

​      "save": [

​        {

​          "annotation": "BaseDBAsyncClient | None",

​          "default": "None",

​          "kind": "POSITIONAL_OR_KEYWORD",

​          "name": "using_db"

​        },

​        {

​          "annotation": "Iterable[str] | None",

​          "default": "None",

​          "kind": "POSITIONAL_OR_KEYWORD",

​          "name": "update_fields"

​        },

​        {

​          "annotation": "bool",

​          "default": "False",

​          "kind": "POSITIONAL_OR_KEYWORD",

​          "name": "force_create"

​        },

​        {

​          "annotation": "bool",

​          "default": "False",

​          "kind": "POSITIONAL_OR_KEYWORD",

​          "name": "force_update"

​        }

​      ],

​      "update_from_dict": [

​        {

​          "annotation": "dict",

​          "default": null,

​          "kind": "POSITIONAL_OR_KEYWORD",

​          "name": "data"

​        }

​      ]

​    },

},

  "success": true

}
```

```json
Get /scan_functions
```

请求参数：

directory：项目根路径,如 D:/P-guard/backend

响应示例

```json
{
  "data": {
    "controller.detectController": [
      {
        "args": [
          "plotId",
          "user"
        ],
        "async": true,
        "name": "validate_plot_access"
      },
      {
        "args": [
          "plotId",
          "name",
          "advice",
          "save_path"
        ],
        "async": true,
        "name": "call_set_log"
      },
      ],
      "controller.logController": [
      {
        "args": [
          "plotId",
          "diseaseName",
          "advice",
          "imageURL"
        ],
        "async": true,
        "name": "set_log"
      },
      {
        "args": [
          "plotId"
        ],
        "async": true,
        "name": "get_logs"
      }
	  ]
    },
  "success": true
}
```

```json
Post /run_unit_test
```

请求体（表单）：

directory：项目根路径,如 D:/P-guard/backend

root: 项目根路径

class_name:service.log

method_name:analyze_plot_details

mock_config:{'service.log.get_prediction_by_name':{'_async_mock':'True','mock_value':'p'}}

excel_file: test_case.xlsx

```
Excel文件格式（参考仓库/backend/resource目录下的.xlsx文件）：
- 第一行：列名（ID、测试方法、测试描述、期望结果、属性名等）
- 第二行：数据类型（对应每列的数据类型）
- 第三行开始：测试数据
```

响应示例

```json
{
  "class": "service.log",
  "description": "ss",
  "message": "单元测试执行完成",
  "method_name": "analyze_plot_details",
  "mock_config": {
    "service.log.get_prediction_by_name": {
      "_async_mock": "True",
      "mock_value": "p"
    }
  },
  "success": true,
  "summary": {
    "failed_cases": 3,
    "pass_rate": "0.0%",
    "passed_cases": 0,
    "total_cases": 3
  },
  "test_method": "ss",
  "test_name": "ss",
  "test_results": [
    {
      "Actual": {
        "disease_count": {},
        "monthly_disease_count": [
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0
        ],
        "plant_disease_count": {},
        "plant_plot_count": {
          "植物A": 1
        },
        "plot_count": 1,
        "prediction": "p"
      },
      "Duration": "0ms",
      "Expected": "{'plot_count': 0, 'plant_plot_count': {}, 'monthly_disease_count': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 'plant_disease_count': {}, 'disease_count': {}, 'prediction': 'mocked_prediction'}",
      "ID": 1,
      "Passed": false
    },
    {
      "Actual": {
        "disease_count": {},
        "monthly_disease_count": [
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0
        ],
        "plant_disease_count": {},
        "plant_plot_count": {
          "植物A": 1
        },
        "plot_count": 1,
        "prediction": "p"
      },
      "Duration": "0ms",
      "Expected": "{'plot_count': 0, 'plant_plot_count': {}, 'monthly_disease_count': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 'plant_disease_count': {}, 'disease_count': {}, 'prediction': 'mocked_prediction'}",
      "ID": 2,
      "Passed": false
    },
    {
      "Actual": {
        "disease_count": {},
        "monthly_disease_count": [
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0
        ],
        "plant_disease_count": {},
        "plant_plot_count": {
          "植物A": 1
        },
        "plot_count": 1,
        "prediction": "p"
      },
      "Duration": "0ms",
      "Expected": "{'plot_count': 0, 'plant_plot_count': {}, 'monthly_disease_count': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], 'plant_disease_count': {}, 'disease_count': {}, 'prediction': 'mocked_prediction'}",
      "ID": 3,
      "Passed": false
    }
  ]
}
```

