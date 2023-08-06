# encoding: UTF-8

"""
Augustus - An event-driven quantitative backtesting and algorithm trading library in Python.

This Project is an open source quantitative trading framework written in Python.
"""

import os

from setuptools import Command,find_packages,setup

class CleanCommand(Command):
    user_options=[]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("rm -vrf ./build ./dist ./*.pyc ./*.egg-info")

setup(
    name="augustus_quant",
    version="1.0.0",
    author="Jialue Chen",
    author_email="jialuechen@outlook.com",
    license="MIT",
    url="https://github.com/jialuechen/augustus",
    description="Quantitative trading framework in Python",
    packages=find_packages(),
    install_requires=["pandas","numpy","pymongo","retry","TA-Lib","arrow","funcy","plotly"]
)