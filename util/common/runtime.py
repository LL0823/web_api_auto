#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/21 17:54
import logging

from util.common.config import Config
from util.helper.login_helper import LoginHelper


class Runtime:
    users_config = {}
    current_user = {}
    logged_users = {}

    @classmethod
    def reset_config(cls):
        """
        重置用户信息
        current_user-当前需要切换的user
        users_config-配置中的users信息
        logged_users-已登录状态账号，有token
        :return:
        """
        cls.current_user = {}
        cls.users_config = {}
        cls.logged_users = {}
        logging.info("重置账号")

    @classmethod
    def set_user_config(cls, config: Config):
        cls.reset_config()
        cls.users_config = config.get('users')
        assert cls.users_config is not None, "未配置任何users信息"

    @classmethod
    def set_current_user(cls, current_user_key='default'):
        if current_user_key not in cls.logged_users.keys():
            cls.__login(current_user_key)
        cls.current_user = cls.logged_users.get(current_user_key)
        logging.info(f"切换至账号->{current_user_key}")

    @classmethod
    def get_current_user(cls):
        """
        获取当前用户信息
        :return:
        """
        return cls.current_user

    @classmethod
    def get_host(cls):
        """
        从当前用户信息中拿到host
        :return:
        """
        return cls.current_user.get('host')

    @classmethod
    def get_token(cls):
        return cls.current_user.get('token')

    @classmethod
    def get_headers(cls):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "access-token": cls.get_token()
        }

        return headers

    @classmethod
    def get_normal_headers(cls):
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        return headers

    @classmethod
    def __login(cls, user_key):
        user = cls.users_config.get(user_key)
        assert user is not None, f"配置信息中没有找到对应的用户信息【{user_key}】"
        user['token'] = LoginHelper.login(user)
        cls.logged_users[user_key] = user
        logging.info(f"登录账号【{user_key}】")
