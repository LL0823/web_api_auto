#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/21 21:19
import logging
import os.path

import yaml


class FileHelper:
    @classmethod
    def get_root_path(cls):
        current_path = __file__
        split_path = current_path.split(os.path.sep)
        return os.path.sep.join(split_path[:-3])

    @classmethod
    def get_path(cls, *paths):
        """
        拼接上根目录
        :param paths: 文件目录地址
        :return: 返回完整的绝对路径
        """
        return os.path.join(cls.get_root_path(), *paths)

    @classmethod
    def read_config_yaml(cls, yaml_path:str, raise_if_not_exist:bool = True):
        """
        从yaml的配置文件中读取配置内容
        :param raise_if_not_exist: 文件不存在时是否抛出异常。在只有全局配置时，读取不到局部配置，能够继续走下去
        :param yaml_path:config配置文件的路径
        :return: 返回从yaml配置文件中读取的
        """
        logging.info(f"正在读取配置文件：{yaml_path}")
        if not os.path.isfile(yaml_path):
            if raise_if_not_exist:
                raise AssertionError(f"配置文件不存在：{yaml_path}")
            else:
                return None
        with open(yaml_path, encoding='utf-8') as f:
            content = yaml.load(f.read(), Loader=yaml.SafeLoader)
        return content
