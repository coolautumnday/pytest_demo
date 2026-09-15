import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "search: 搜索模块用例"
    )
    config.addinivalue_line(
        "markers", "login: 登录模块用例"
    )
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试用例"
    )
    config.addinivalue_line(
        "markers", "regression: 回归测试用例"
    )

# 用例执行前，自动创建report文件夹，防止不存在报错
@pytest.fixture(autouse=True, scope="session")
def create_report_dir():
    import os
    if not os.path.exists("report"):
        os.mkdir("report")
