from flask import Flask
from app.routes.homework import homework_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(homework_bp)

if __name__ == '__main__':
    app.run(debug=True)