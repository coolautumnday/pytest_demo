import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# @pytest.mark.parametrize 给fixture传参，指定打开settings
@pytest.mark.parametrize("app_driver", ["settings"], indirect=True)
def test_open_settings(app_driver):
    driver = app_driver
    wait = WebDriverWait(driver, 10)
    ele = wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("南桥挽琴")')))
    assert ele.is_displayed()
    print('成功打开设置页面')