import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 指定打开apidemos
@pytest.mark.parametrize("app_driver", ["apidemos"], indirect=True)
def test_open_apidemo(app_driver):
    driver = app_driver
    wait = WebDriverWait(driver,10)
    ele = wait.until(EC.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("App")')))
    assert ele.is_displayed()
    print('成功打开指定APP页面')