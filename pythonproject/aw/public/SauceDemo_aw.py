from playwright.sync_api import Page, expect
import logging

from aw.public.public_aw import check_result

logging.basicConfig(level=logging.INFO)

class public_aw:
    def __init__(self, page: Page):
        self.page = page

    @check_result('input信息失败')
    def input_message(self, element, input_text=None, timeout=5000):
        """
        通用输入框封装方法
        :param get_type: 定位类型 label / test_id / css / text
        :param type_value: 定位值
        :param input_text: 需要输入的文本
        :param timeout: 超时时间ms，默认5000
        """
        # 判断传入是不是Saucedemo实例
        get_type = element.get_type
        type_value = element.name
        # 如果外部传了value，优先使用；否则使用model内的value
        fill_text = input_text if input_text is not None else element.value

        try:
            # 1. 根据类型获取元素
            if get_type == 'label':
                page_inp = self.page.get_by_label(type_value)
            elif get_type == 'test_id':
                page_inp = self.page.get_by_test_id(type_value)
            elif get_type == 'css':
                page_inp = self.page.locator(type_value)
            elif get_type == 'text':
                page_inp = self.page.get_by_text(type_value)
            else:
                raise ValueError(f"目前不支持的定位类型: {get_type}，想要自己加")

            # 等待元素
            if timeout:
                page_inp.wait_for(timeout=timeout)
            else:
                page_inp.wait_for()
            page_inp.clear()
            page_inp.fill(fill_text)
            logging.info(f"输入成功：{fill_text}")

        except Exception as e:
            logging.error(f"输入失败：{e}")
            raise


    def check_is_visible(self, value, fail_msg: str):
        """
        :param
        value: 元素对象
        fail_msg: 自定义失败提示文案
        :return: bool，True = 校验通过；False = 校验失败
        """
        try:
            return expect(value).to_be_visible()
        except AssertionError:
            return AssertionError(fail_msg)

