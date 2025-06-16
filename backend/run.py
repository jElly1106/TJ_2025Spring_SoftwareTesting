from flask import Flask
from app.routes.homework import homework_bp
from app.routes.unit import unit_bp
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(homework_bp)
app.register_blueprint(unit_bp)
if __name__ == '__main__':
    app.run(debug=True)