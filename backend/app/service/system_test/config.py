"""
E2E测试配置管理类
"""
import os
from typing import Dict, Any

from app.static.system_test import DEFAULT_TEST_CONFIG


class E2ETestConfig:
    """E2E测试配置管理类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._set_defaults()
    
    def _set_defaults(self):
        """设置默认配置值"""
        for key, value in DEFAULT_TEST_CONFIG.items():
            if key not in self.config:
                self.config[key] = value
    
    def get(self, key: str, default=None):
        """获取配置项值"""
        return self.config.get(key, default)
    
    def get_base_url(self) -> str:
        """获取基础URL"""
        return self.config['base_url']
    
    def validate(self):
        """验证配置的完整性"""
        required_fields = ["base_url", "test_username", "test_password"]
        for field in required_fields:
            if not self.config.get(field):
                raise ValueError(f"缺少必要配置项: {field}")
    
    def update(self, config: Dict[str, Any]):
        """更新配置"""
        self.config.update(config)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.config.copy()
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"E2ETestConfig({self.config})"
    
    def __repr__(self) -> str:
        """开发者表示"""
        return self.__str__()