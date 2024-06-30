#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/22 11:21
import hashlib

import requests
from util.helper.resp_helper import RespHelper


class LoginHelper:
    @classmethod
    def login(cls, user_config):
        """
        用户登录，返回token供其它接口使用
        :param user_config:
        :return: token
        """
        host = user_config.get('host')
        username = user_config.get('name')
        password = user_config.get('password')
        # url = f"{host}/login"
        # params = {"username": username, "password": cls.__get_password_md5(password)}
        # resp = requests.get(url,params)
        # result = RespHelper(resp)
        # token = result.get("$.data.accessToken")
        # todo 目前没有接口可以获取token，先返回个假的跑一跑
        token = '123abc'
        return token

    @classmethod
    def __get_password_md5(cls, password: str):
        """
        获取密码md5加密
        :param password:
        :return:
        """
        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        return m.hexdigest()
