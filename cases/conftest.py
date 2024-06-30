#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: liu
# time: 2024/4/23 16:59
import pytest
from py.xml import html


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    """
    增加报告表头
    """
    cells.insert(3, html.th('description', class_='sortable description', col='description'))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """
    插入表数据
    """
    cells.insert(3, html.td(report.description, class_='col-description'))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    数据处理
    :param item: 运行的方法对象
    """
    outcome = yield
    report = outcome.get_result()

    report.description = ""
    for mark in item.own_markers:
        if mark.name == "allure_label":
            report.description = mark.args[0]

    # if os.environ.get('IS_RUN_CASE') == "YES" and sys.platform == 'win32' or 1==1:
    report.nodeid = report.nodeid.encode("unicode_escape").decode("utf-8")

