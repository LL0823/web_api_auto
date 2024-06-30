#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/18 15:55
import logging

import pytest
import os
import typer

from util.helper.file_helper import FileHelper

app = typer.Typer()


def send_email():
    pass


@app.command()
def main(env: str = None, test_cases: str = typer.Option('cases', help="需要运行的case文件,多个以英文逗号分隔"),
         pytest_marker: str = None, reruns: int = None,
         reruns_delay: int = None, repeat_scope: str = None, junitxml: str = None):
    """

    :param env: 选择运行的环境，默认的config.yaml
    :param test_cases: 选择需要运行的case文件
    :param pytest_marker: pytest参数：选择运行时要限制的marker
    :param reruns: pytest参数：reruns
    :param reruns_delay: pytest参数：reruns_delay
    :param repeat_scope: pytest参数：repeat_scope
    :param junitxml: pytest参数：junitxml
    :return:
    """
    logging.info('正在执行pytest')
    # allure报告相关路径
    allure_result_dir = FileHelper.get_path('allure-results')
    allure_report_dir = FileHelper.get_path('allure-report')
    # 根据传入的环境，取对应配置文件。
    if env:
        os.environ['config-env'] = env
    # 1. pytest运行参数拼接，调用pytest.main方法触发用例执行
    pytest_params = [
        "--alluredir", allure_result_dir,
        "-vs", *test_cases.split(','),
    ]
    if pytest_marker:
        pytest_params.append(f"-m {pytest_marker}")
    if reruns and reruns_delay:
        pytest_params.append(f"--reruns={reruns}")
        pytest_params.append(f"--reruns-delay={reruns_delay}")
    if repeat_scope:
        pytest_params.append(f"--repeat-scope={repeat_scope}")
    if junitxml:
        pytest_params.append(f"--junitxml={junitxml}")
    logging.info("pytest参数: %s", pytest_params)
    pytest.main(pytest_params)

    # 2. 使用allure命令生成测试报告 ：allure generate 数据路径文件 -o html路径文件 -c
    cmd = 'allure generate {} -o {} -c'.format(allure_result_dir, allure_report_dir)
    logging.info('执行命令生成报告：%s', cmd)
    os.system(cmd)
    logging.info('报告生成完毕，报告路径：%s', allure_report_dir)

    # todo 报告结果邮件发送
    send_email()


if __name__ == '__main__':
    # 参数从命令行读取，利用typer包
    app()
    # 也可以使用typer.run(main)
