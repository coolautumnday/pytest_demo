import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
@pytest.mark.no_browser
def test_demo_baidu(page: Page):
    page.goto("https://www.baidu.com")
    page.wait_for_load_state("networkidle")

    # 角色定位：文本输入框 textbox
    search_input = page.get_by_role("textbox")
    search_input.wait_for(state="visible", timeout=10000)
    search_input.fill("Playwright自动化")

    page.get_by_role("button", name="百度一下").click()
    page.wait_for_timeout(2000)
