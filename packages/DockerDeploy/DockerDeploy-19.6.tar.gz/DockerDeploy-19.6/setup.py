#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""
File:   setup.py
Author: Lijiacai (1050518702@qq.com)
Date: 2019-01-02
Description:
   setup tool
"""

import os
import sys

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/" % cur_dir)

from setuptools import setup
from setuptools import find_packages

long_description="""
	安装部署工具
			pip install DockerDeploy
	安装docker
			deploy --docker-install
	卸载docker
			deploy --docker-uninstall
	重启docker
			deploy --docker-restart
	启动docker
			deploy --docker-start
	终止docker
			deploy --docker-stop
	查看docker基础命令
			deoploy --docker-command
	创建一个部署项目
			deploy --make-project 
				e.g deploy --make-project test
	查看帮助
			deply --help"""

setup(
    name="DockerDeploy",
    version="19.6",
    keywords=("docker", "deploy", "dockerdeploy", "DockerDeploy"),
    description="Docker deployment framework",
    long_description=long_description,
    license="MIT License",

    url="https://github.com/lijiacaigit/docker_deploy_command",
    author="Lijiacai",
    author_email="1050518702@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],  # 这个项目需要的第三方库
    scripts=["bin/deploy"]
)
