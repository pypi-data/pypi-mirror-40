
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "funddata",      #这里是pip项目发布的名称
    version = "1.0.3",  #版本号，数值大的会优先被pip
    keywords = ("pip", "funddata"),
    description = "A stockdata database api",
    long_description = "A stockdata database api ",
    license = "guopw Licence",

    url = "https://github.com/guopw/funddata",     #项目相关文件地址，一般是github
    author = "guopw",
    author_email = "154221886@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any"
          #这个项目需要的第三方库
)
