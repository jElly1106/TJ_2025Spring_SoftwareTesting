from flask import Blueprint, request, jsonify
import os
from app.data.static_data import HOMEWORK_CODES

homework_bp = Blueprint('homework', __name__)

@homework_bp.route('/homework/code', methods=['GET'])
def get_homework_code():
    """
    获取题目的初始代码
    查询参数：
    - problem: 题目名称 (triangle_judge, computer_selling, telecom_system, calendar_problem)
    
    返回格式：
    {
        "success": true/false,
        "code": "代码字符串",
        "message": "提示信息"
    }
    """
    try:
        problem = request.args.get('problem')
        
        if not problem:
            return jsonify({
                "success": False,
                "code": "",
                "message": "缺少problem参数"
            }), 400
        
        if problem not in HOMEWORK_CODES:
            available_problems = list(HOMEWORK_CODES.keys())
            return jsonify({
                "success": False,
                "code": "",
                "message": f"题目不存在。可用题目：{', '.join(available_problems)}"
            }), 404
        
        return jsonify({
            "success": True,
            "code": HOMEWORK_CODES[problem],
            "message": "获取代码成功"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "code": "",
            "message": f"服务器错误：{str(e)}"
        }), 500