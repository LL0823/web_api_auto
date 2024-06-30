#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/21 18:14
import inspect
import logging
import os

import pytest

from util.common.config import Config
from util.common.runtime import Runtime
from util.helper.file_helper import FileHelper


class BaseCase:
    @pytest.fixture(scope="module")
    def config(self):
        """
        读取配置文件，如果局部和全局字段相同，取局部字段值
        :return: yaml中读取的字典格式
        """
        # 通过runcase中的main方法，获取命令行输入的环境参数，来判断取那一份配置文件。
        env_config = os.environ.get("config-env")
        config_file_name = "config.yaml"
        if env_config:
            config_file_name = f"config-{env_config}.yaml"

        # 全局配置
        global_config_dir = FileHelper.get_path("cases", "global_config")
        global_config_file = os.path.join(global_config_dir,config_file_name)
        result_config = FileHelper.read_config_yaml(global_config_file)
        # 局部配置
        sub_class_path = inspect.getfile(self.__class__)
        local_config_dir = os.path.split(sub_class_path)[0]
        local_config_file = os.path.join(local_config_dir, "config", config_file_name)
        local_config = FileHelper.read_config_yaml(local_config_file, raise_if_not_exist=False)
        assert result_config is not None or local_config is not None, f"未读取到配置文件，请检查配置文件：{global_config_file}、{local_config_file}"
        # 局部变量覆盖全局变量
        if result_config and local_config:
            result_config.update(local_config)
        elif result_config is None:
            result_config = local_config
        yield Config(result_config)

    @pytest.fixture
    def _set_all_users(self, config):
        """
        这个方法不确认要不要加自动执行，因为是在下面一个配置了自动执行中调用的fixture方法
        :param config:
        :return:
        """
        self.user_config = config.get('users')
        assert self.user_config is not None, "未配置任何users信息"
        Runtime.set_user_config(config)

    @pytest.fixture(scope='function', autouse=True)
    # todo 这里先把自动调用生成token注释了。目前开放的接口没有能给我生成token的
    def _set_default_user(self, _set_all_users):
        """
        设置为自动执行，每个用例都会自动执行该fixture方法
        :param _set_all_users:
        :return:
        """
        get_user_info = Runtime.get_current_user()
        if get_user_info.get('o_c_code') == 'YES':
            logging.info("无需切换成默认用户")
        else:
            Runtime.set_current_user('default')

    @classmethod
    def change_to_user(cls, username: str):
        """
        切换账号信息，根据config文件中users下面的key值进行切换
        :param username:
        :return:
        """
        Runtime.set_current_user(username)

    @classmethod
    def get_current_user(cls):
        return Runtime.get_current_user()
