#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/18 15:50
import allure
import pytest
from util.common.case.base_case import BaseCase
from api.qq_fanyi_api import QQApi


@allure.epic("qq翻译")
@allure.feature("feature层级-qq翻译接口")
class TestFirst(BaseCase):
    def test_get_qq_fanyi_success(self, config):
        """
        待办
        1、把url的读取放到配置中，方便切换不同环境
        2、把请求响应的内容进行封装，方便进行断言===先做这个
        3、头部信息进行一个封装
        4、写一下runcase方法
        5、断言的封装也可以整一下，不急
        """
        fanyi_text = "test"
        result = QQApi().get_qq_fanyi(fanyi_text)
        result.assert_http_code()
        assert result.get('$.result.sourceText') == fanyi_text, "查询的文本与返回的文本进行校验"

    @allure.story('参数化例子一个')
    @pytest.mark.parametrize("text", ['hello', 'One', 'this is an apple'])
    def test_param_qq_fanyi(self, text):
        result = QQApi().get_qq_fanyi(text)
        result.assert_http_code()
        result_text = result.get('$.result.sourceText')
        assert result_text == text, f"翻译的文案不对:{result_text}"
