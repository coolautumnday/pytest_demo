import base64

import pytest
from playwright.sync_api import Page

from aw.public.SauceDemo_aw import public_aw

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

# # 用例执行前，自动创建report文件夹，防止不存在报错
# @pytest.fixture(autouse=True, scope="session")
# def create_report_dir():
#     import os
#     if not os.path.exists("report"):
#         os.mkdir("report")

@pytest.fixture(scope="function")  # function：每个测试函数都会重新执行一次
def get_pa(request, page: Page):
    def _get_pa(url):
        page.goto(url, wait_until="domcontentloaded")
        pa = public_aw(page)
        return page, pa

    if request.node.get_closest_marker("no_browser"):
        yield
        return
    yield _get_pa

    # 后置：用例执行完成之后执行
    page.context.clear_cookies()
    page.evaluate("localStorage.clear()")
    page.evaluate("sessionStorage.clear()")
    page.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest钩子：捕获用例执行结果，失败时截图，嵌入html报告
    """
    # 执行所有后置钩子
    outcome = yield
    rep = outcome.get_result()

    # 只在call阶段（用例实际执行）并且用例失败时处理
    if rep.when == "call" and rep.failed:
        # 获取当前用例的page对象
        page = item.funcargs.get("page", None)
        if page:
            try:
                # 截图，返回bytes
                screenshot_bytes = page.screenshot(full_page=True)
                # base64编码，嵌入html（不需要单独图片文件）
                b64 = base64.b64encode(screenshot_bytes).decode()
                html = f'<div><img src="data:image/png;base64,{b64}" style="width:800px"/></div>'
                # 添加到报告extra，pytest-html会渲染图片
                rep.extra = getattr(rep, "extra", [])
                from pytest_html import extras
                rep.extra.append(extras.html(html))
            except Exception as e:
                print(f"截图失败：{e}")