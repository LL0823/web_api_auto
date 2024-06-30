#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/21 17:35
from util.common.runtime import Runtime


class BaseApi:
    @classmethod
    def get_host(cls) -> str:
        return Runtime.get_host()

    @classmethod
    def get_token(cls) -> str:
        return Runtime.get_token()

    @classmethod
    def get_header(cls) -> dict:
        return Runtime.get_headers()

    @classmethod
    def get_normal_headers(cls) -> dict:
        return Runtime.get_normal_headers()

