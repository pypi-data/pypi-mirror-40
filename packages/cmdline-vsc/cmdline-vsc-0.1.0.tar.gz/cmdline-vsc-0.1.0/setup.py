# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('vsc/vsc.py').read(),
    re.M
).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="cmdline-vsc",
    packages=["vsc"],
    entry_points={
        "console_scripts": ['vsc = vsc.vsc:main']
    },
    version=version,
    description="Python command line application bare bones template.",
    long_description=long_descr,
    author="Cmitru",
    author_email="carmen.mitru@googlemail.com"
)
