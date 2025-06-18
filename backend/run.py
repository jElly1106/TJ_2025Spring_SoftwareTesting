from flask import Flask

from app.routes.homework import homework_bp
from app.routes.admin_test import admin_test_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(homework_bp)
app.register_blueprint(admin_test_bp)

if __name__ == '__main__':
    app.run(debug=True)