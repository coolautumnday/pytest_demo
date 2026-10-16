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
        :param element: Model控件
        :param input_text: 需要输入的文本
        :param timeout: 超时时间ms，默认5000
        """
        get_type = element.get_type
        type_name = element.type_name
        # 如果外部传了value，优先使用；否则使用model内的value
        fill_text = input_text if input_text is not None else element.type_value

        try:
            # 1. 根据类型获取元素
            if get_type == 'label':
                page_inp = self.page.get_by_label(type_name)
            elif get_type == 'test_id':
                page_inp = self.page.get_by_test_id(type_name)
            elif get_type == 'css':
                page_inp = self.page.locator(type_name)
            elif get_type == 'text':
                page_inp = self.page.get_by_text(type_name)
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

    @check_result('控件元素查找失败')
    def get_ElementControl(self, element, role_attribute: dict = None):
        """
        element: model元素对象
        :return: bool，True = 校验通过；False = 校验失败
        """
        get_type = element.get_type
        type_name = element.type_name
        role_attribute = role_attribute if role_attribute is not None else element.type_value
        # 如果外部传了value，优先使用；否则使用model内的value
        if get_type == 'label':
            page_ele = self.page.get_by_label(type_name)
        elif get_type == 'test_id':
            page_ele = self.page.get_by_test_id(type_name)
        elif get_type == 'text':
            page_ele = self.page.get_by_text(type_name)
        elif get_type == 'title':
            page_ele = self.page.get_by_title(type_name)
        elif get_type == 'alt_text':
            page_ele = self.page.get_by_alt_text(type_name)
        elif get_type == 'placeholder':
            page_ele = self.page.get_by_placeholder(type_name)
        elif get_type == 'role':
            page_ele = self.page.get_by_role(type_name, **role_attribute)
        elif get_type == 'css':
            page_ele = self.page.locator(role_attribute)
        elif get_type == 'locator':
            page_ele = self.page.locator(role_attribute)
        else:
            raise ValueError(f"目前不支持的定位类型：{get_type}，想要自己加")
        return page_ele


    def check_is_visible(self, value, is_except=True, fail_msg: str=None):
        """
        value: 元素对象
        fail_msg: 自定义失败提示文案
        :return: bool，True = 校验通过；False = 校验失败
        """
        try:
            if is_except:
                return expect(value).to_be_visible()
            else:
                return expect(value).not_to_be_visible()
        except AssertionError:
            return AssertionError(fail_msg)

