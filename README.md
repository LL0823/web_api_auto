# 项目介绍
## web的接口自动化框架构建
- 本项目实现接口自动化的技术选型：pytest+request+allure ，主要是针对qq翻译接口作为demo来开展的，
- 通过 request进行api自动化框架构建，使用 Pytest 作为测试执行器，
- 使用 Allure 来生成测试报告。程序入口为：runcase.py文件

# 文件目录

- api/                          # 接口统一封装目录
    - __init__.py
    - qq_fanyi_api.py           # 接口封装
- cases/                         # 自动化用例目录
    - global_config/            # 全局配置(小横线后对应不同环境，默认环境不用加后缀)
        - config.yml
        - config-pre.yml
    - test_qq_fanyi/            # 按功能划分用例
        - config/               # 局部配置(与全局字段相同则使用覆盖全局配置)
            - config.yml
            - config-pre.yml
        - __init__.py
        - test_first_case.py    # 具体用例
    - conftest.py               # pytest下的指定文件使用
- utils/                        # 工具类
    - common/                   # api和case的基类都在这里面
    - __init__.py
    - helper/                   # 页面封装的父类，对操作进行了一些二次封装
      - config.py                 # 对yaml文件中读取的数据方便进行jsonpath读取的帮助类
      - datas_helper.py           # 用例数据驱动帮助类
      - driver_helper.py          # 驱动帮助类，还未完成，暂时无用
      - file_helper.py            # 文件帮助类
- .gitignore                    # git配置文件
- pytest.ini                    # pytest配置文件
- requirements.txt              # 依赖配置文件
- runcase.py                    # 程序入口

# runcase参数使用
## 不传参数使用默认python run_case.py即可跑起来
- env参数

    例：python run_case.py --env="pre"
- test-cases参数

    参数：--test-cases，执行多个用例文件/目录，使用英文逗号隔开
  - 执行单个用例
  
  例：python run_case.py --test-cases="case/test_demo/test_a.py"
  - 执行多个用例
  
  例：python run_case.py --test-cases="case/test_demo/test_a.py,case/test_demo/test_b.py"
- 其它pytest的原有参数

    pytest_marker、 reruns、reruns_delay、repeat_scope、junitxml

