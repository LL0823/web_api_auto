#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/18 16:44
import json
import logging
from jsonpath import jsonpath


class RespHelper:
    def __init__(self, resp):
        self.resp = resp
        self.http_code = resp.status_code
        # http响应数据，如果响应数据不能转换为json，可以使用此字段
        try:
            self.content = resp.content.decode('utf-8')
        except Exception as e:
            logging.info(f"解析resp.content失败，可能原因：结果要二进制文件，{e}")
            self.content = None
        self.text = resp.text

        # http响应数据转换成json格式，如果返回None，则不是json格式
        self.json = None
        try:
            self.json = resp.json()
        except ValueError:
            logging.warning("返回的resp不是json格式", resp.request.url, resp.request.method)

        # 把请求内容打印日志，方便排查问题
        logging.info(f"【{resp.request.method}】:{resp.request.url}")
        if resp.request.body:
            logging.info(str(resp.request.body))
        data = json.dumps(self.json) if self.json else self.content
        # 转换unicode日志显示中文
        try:
            data = data.encode().decode('unicode_escape')
        except Exception as e:
            logging.warning(f"响应结果响应转码中文失败：{e}")
        logging.info(f"【{resp.status_code}】:{data}")

    def assert_http_code(self, http_code: int = 200):
        assert self.http_code == http_code, f"http响应码错误，期望是：{http_code}，实际是：{self.http_code}"

    def assert_resp_code(self, resp_code: int = 200):
        code = self.get('code')
        assert code == resp_code, f"响应的resp_code错误，期望值是:{resp_code}，实际是：{code}"

    def assert_resp(self, json_path: str, data: str, message: str = ''):
        get_data = self.get(json_path)
        if message == '':
            message = f"{json_path}的预期值是{data}，但是实际值是{get_data}"
        assert str(data) == str(get_data), message

    def assert_resp_in(self, json_path: str, data: str, message: str = ''):
        get_data_list = self.get_multi(json_path)
        result = False
        if message == '':
            message = f"{json_path}的预期值是{data}，但是实际值是{get_data_list}"
        for i in get_data_list:
            if data == str(i):
                result = True
        assert result, message

    def get(self, json_path):
        self._assert_json()
        value = jsonpath(self.json, json_path)
        assert value, f"【{json_path}】实际未取到任何值：{self.json}"
        assert len(value) == 1, f"【{json_path}】取到的数量不止一个"
        return value[0]

    def get_multi(self, json_path):
        self._assert_json()
        value = jsonpath(self.json, json_path)
        assert value, f"【{json_path}】实际未取到任何值：{self.json}"
        assert len(value) >= 1, f"【{json_path}】:实际获取值少于1个"
        return value

    def _assert_json(self):
        """
        通过断言判断是否成功转换成json格式，没有用抛异常的方式，直接用断言来处理
        :return:
        """
        # if self.json is None:
        #     raise Exception("响应消息不是json格式，没法提取字段")
        assert self.json is not None, "响应消息不是json格式，没法提取字段"
