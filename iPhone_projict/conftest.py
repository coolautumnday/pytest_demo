# conftest.py
import subprocess
import pytest
import time
import socket
import os
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options

# # 检测端口是否开放
# def is_port_open(host="127.0.0.1", port=4723):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.settimeout(1)
#     try:
#         s.connect((host, port))
#         return True
#     except Exception:
#         return False
#     finally:
#         s.close()

# # session级：整个测试会话只启动一次appium服务
# @pytest.fixture(scope="session", autouse=True)
# def appium_server():
#     # 启动appium，端口4723
#     # proc = subprocess.Popen(
#     #     ["appium", "-p", "4723"], shell=True,
#     #     creationflags=subprocess.CREATE_NO_WINDOW  # Windows隐藏黑框，mac/linux删除此行
#     # )
#     proc = subprocess.Popen(
#         [r"C:\Users\doushouchang\AppData\Roaming\npm\appium", "-p", "4723"],
#         creationflags=subprocess.CREATE_NO_WINDOW
#     )
#
#     print("=== 正在启动Appium服务，等待端口就绪 ===")
#     # 最多等待10秒
#     for _ in range(10):
#         if is_port_open("127.0.0.1", 4723):
#             print("✅ Appium服务就绪，4723端口可连接")
#             break
#         time.sleep(1)
#     else:
#         raise Exception("❌ Appium启动超时，4723端口无法连接！")
#
#     yield  # 等待所有用例执行
#
#     # 全部用例跑完，关闭appium进程
#     proc.terminate()
#     proc.wait()
#     print("\n=== Appium服务已关闭 ===")

# 定义两个APP的配置字典，集中管理
APP_CONFIG = {
    "settings": {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "test_device",
        "appium:appPackage": "com.android.settings",
        "appium:appActivity": ".Settings",
        "appium:noReset": True,
        "appium:unicodeKeyboard": True,
        "appium:resetKeyboard": True,
        "appium:skipServerInstallation": True,
        "appium:skipDeviceInitialization": True,
        # 新增下面两行，解决noReset不拉起app的问题
        "appium:forceAppLaunch": True,
        "appium:shouldTerminateApp": True,
        # 兼容不同手机的设置主页面
        "appium:appWaitPackage": "com.android.settings",  # 新增！明确等待哪个包
        "appium:appWaitActivity": "io.appium.android.apis.*",
        'newCommandTimeout': 90
    },
    "apidemos": {
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "test_device",
        "appium:appPackage": "io.appium.android.apis",
        "appium:appActivity": ".ApiDemos",
        "appium:noReset": True,
        "appium:unicodeKeyboard": True,
        "appium:resetKeyboard": True,
        "appium:skipServerInstallation": True,
        "appium:skipDeviceInitialization": True,
        # 新增下面两行，解决noReset不拉起app的问题
        "appium:forceAppLaunch": True,
        "appium:shouldTerminateApp": True,
        # 兼容不同手机的设置主页面
        "appium:appWaitPackage": "io.appium.android.apis",  # 新增
        "appium:appWaitActivity": "io.appium.android.apis.*",
        'newCommandTimeout': 90
    }
}


@pytest.fixture(scope="function")
def app_driver(request):
    app_name = request.param
    desired_caps = APP_CONFIG[app_name]
    # 核心改动：使用 UiAutomator2Options 加载cap，用options参数传入
    options = UiAutomator2Options().load_capabilities(desired_caps)
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    print('\ndrivvv', driver)

    yield driver

    print('requests', request.node.rep_call, type(request.node.rep_call))
    # print('requestsall1', vars(request.node.rep_call))

    print('ssssss', driver.session_id)
    print('driver', vars(driver))

    # ========== teardown增加异常捕获，防止卡死 ==========
    try:
        # 判断用例失败，执行截图
        if request.node.rep_call.failed:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = os.path.join("./report/", timestamp, '/')
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            save_path = os.path.join(screenshot_dir, f"{request.node.nodeid}_{timestamp}.png")
            # 截图单独try，就算截图失败，也不影响后面quit
            try:
                driver.save_screenshot(save_path)
                print(f"📸 失败截图保存：{save_path}")
            except Exception as e:
                print(f"⚠️ 截图命令异常：{e}")
    finally:
        try:
            driver.quit()
        except Exception as e:
            print(f"quit异常 {e}")

        # 优先adb强制停止被测app，绕开appium内部关闭逻辑
        import subprocess
        subprocess.run(["adb", "shell", "am", "force-stop", desired_caps["appium:appPackage"]])
        subprocess.run(["adb", "shell", "am", "force-stop", "io.appium.uiautomator2.server"], capture_output=True)

        try:
            driver.quit()
            print("✅ driver正常quit，session关闭")
        except Exception as e:
            print(f"❌ driver.quit()阻塞/异常，强制释放: {e}")
            # 可选：adb杀掉uiautomator2服务，清理占用
            # subprocess.run(["adb", "shell", "am", "force-stop", "io.appium.uiautomator2.server"])
            subprocess.run(["adb", "shell", "am", "force-stop", app_name['appium:appPackage']])


# pytest钩子函数：用例执行结果标记，给request.node.rep_call提供状态
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
