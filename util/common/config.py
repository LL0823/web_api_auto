#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/21 20:55
import copy

from jsonpath import jsonpath


class Config:
    def __init__(self, data):
        self.data = data

    def get(self, json_path: str):
        value = jsonpath(self.data, json_path)
        assert value, f"【{json_path}】实际未取到任何值"
        assert isinstance(value, list), f"【{json_path}】未知结果"
        assert len(value) == 1, f"【{json_path}】实际获取值数量不唯一【{value}】"
        copy_value = copy.deepcopy(value[0])
        return copy_value

    def get_multi(self, json_path: str):
        value = jsonpath(self.data, json_path)
        assert value, f"【{json_path}】实际未取到任何配置"
        assert isinstance(value, list), f"【{json_path}】未知结果【{value}】"
        assert len(value) >= 1, f"【{json_path}】未取到任何值"
        return value
