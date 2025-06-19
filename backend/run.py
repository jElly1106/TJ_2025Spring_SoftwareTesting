from flask import Flask

from app.routes.homework import homework_bp
from app.routes.admin_test import admin_test_bp
from app.routes.unit import unit_bp
from app.routes.plot_test import plot_test_bp
from app.routes.detect_controller_test import detect_test_bp
from app.routes.plot_controller_test import plot_controller_test_bp
from app.routes.log_controller_test import log_test_bp
from app.routes.system_test import system_test_bp

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(homework_bp)
app.register_blueprint(admin_test_bp)
app.register_blueprint(unit_bp)
app.register_blueprint(plot_test_bp)
app.register_blueprint(detect_test_bp)
app.register_blueprint(plot_controller_test_bp)
app.register_blueprint(log_test_bp)
app.register_blueprint(system_test_bp)

if __name__ == '__main__':
    app.run(debug=True)