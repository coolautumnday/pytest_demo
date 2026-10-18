import pytest
import allure
import logging
import traceback
from playwright.sync_api import Page
from aw.Business.business_aw import Bus_aw
from _pytest.logging import LogCaptureFixture


def pytest_addoption(parser):
    parser.addoption("--report-path", action="store", default="./report/tmp", help="测试报告根路径")


# pytest报告钩子，用于读取用例执行结果
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    # -------------------新增：用例执行失败时打印报错信息到logging.info-------------------
    # 只处理call阶段（真正执行用例，不是setup/teardown）且失败
    if rep.when == "call" and rep.failed:
        case_name = item.nodeid
        logging.info("=" * 80)
        logging.info(f"【用例执行失败】用例名称: {case_name}")
        logging.info(f"执行结果: FAILED")

        if call.excinfo is not None:
            # 获取异常类型、异常信息
            exc_type = call.excinfo.type
            exc_value = call.excinfo.value
            logging.info(f"异常类型: {exc_type.__name__}")
            logging.info(f"异常信息: {exc_value}")

            # 获取堆栈，取最关键帧（报错实际代码位置）
            tb = call.excinfo.tb
            if tb is not None:
                # 遍历到最内层堆栈帧
                tb_frame = traceback.extract_tb(tb)[-1]
                err_filename = tb_frame.filename
                err_lineno = tb_frame.lineno
                err_func_name = tb_frame.name
                logging.info(f"报错文件: {err_filename}")
                logging.info(f"报错行号: {err_lineno}")
                logging.info(f"报错函数: {err_func_name}")

        # 失败发生阶段
        logging.info(f"报错发生阶段: {rep.when}")
        logging.info("=" * 80 + "\n")


# 封装带自动截图的step
class ScreenshotStep:
    def __init__(self, page: Page):
        self.page = page

    def step(self, name: str):
        return self._StepContext(self.page, name)

    class _StepContext:
        def __init__(self, page: Page, step_name: str):
            self.page = page
            self.step_name = step_name
            self._ctx = allure.step(step_name)

        def __enter__(self):
            self._ctx.__enter__()

        def __exit__(self, exc_type, exc_val, exc_tb):
            try:
                if not self.page.is_closed():
                    png_data = self.page.screenshot(full_page=True)
                    allure.attach(
                        png_data,
                        name=f"截图：{self.step_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
            except Exception as e:
                logging.info(f"步骤截图跳过: {e}")
            return self._ctx.__exit__(exc_type, exc_val, exc_tb)


@pytest.fixture(autouse=True)
def my_step(page: Page, request):
    """注入到每个用例，step() 自动截图"""
    step_wrapper = ScreenshotStep(page)
    request.node.my_step = step_wrapper
    yield step_wrapper


@pytest.fixture(scope="function")
def page_start(request, page: Page):
    def _get_pa(url: str) -> tuple[Page, Bus_aw]:
        page.goto(url)
        page.context.clear_cookies()
        page.evaluate("localStorage.clear()")
        page.evaluate("sessionStorage.clear()")
        po = Bus_aw(page)
        return page, po

    yield _get_pa
    rep = request.node.rep_call
    if rep.failed:
        # 失败兜底截图
        try:
            png = page.screenshot(full_page=True)
            allure.attach(png, name="用例失败兜底截图", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            pass
    else:
        page.context.clear_cookies()
        page.evaluate("localStorage.clear()")
        page.evaluate("sessionStorage.clear()")


@pytest.fixture(autouse=True)
def attach_log_to_allure(caplog: LogCaptureFixture):
    yield
    log_text = "\n".join(
        f"{record.asctime} {record.levelname} {record.name}: {record.message}" for record in caplog.records)
    if log_text:
        allure.attach(
            log_text,
            name="用例完整运行日志",
            attachment_type=allure.attachment_type.TEXT
        )


@pytest.fixture(autouse=True)
def attach_timestamp_log_to_allure(caplog: LogCaptureFixture):
    """
    每个用例结束后，把本用例全部日志带上【时间戳】存入allure附件
    """
    yield
    # 构造格式化器，和控制台输出格式保持一致
    log_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    log_lines = []
    for record in caplog.records:
        line = log_formatter.format(record)
        log_lines.append(line)
    full_log_text = "\n".join(log_lines)
    if full_log_text.strip():
        allure.attach(
            body=full_log_text,
            name="用例完整日志(带时间戳)",
            attachment_type=allure.attachment_type.TEXT
        )
