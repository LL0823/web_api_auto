#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/23 9:38
import requests

from util.common.api.base_api import BaseApi
from util.helper.resp_helper import RespHelper


class QQApi(BaseApi):
    def get_qq_fanyi(self, source_text):
        url = self.get_host() + 'txt/QQFanyi'
        param = {"sourceText": source_text}
        headers = self.get_normal_headers()
        resp = requests.get(url, params=param, headers=headers)
        return RespHelper(resp)


