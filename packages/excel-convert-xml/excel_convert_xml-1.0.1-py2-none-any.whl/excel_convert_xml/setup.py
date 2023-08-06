# -*- coding:utf-8 -*-
# from distutils.core import setup
import os
from setuptools import setup, find_packages

def find_py_modules():
    modules = []
    for py in os.listdir(os.getcwd()):
        if py.endswith(".py"):
            module_name = py.split(".")[0]
            if module_name != "setup" and module_name != "__init__":
                modules.append(module_name)
    return modules

# 配置文件加載，需要添加絕對路勁
# data_files = [('OnePiece','OnePiece/diff2html/deps/codeformats/xcode.css')]

setup(
    name='excel_convert_xml',
    version='1.0.0',
    description='excel testcase convert testrail xml file',
    long_description='excel testcase convert testrail xml file',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    # py_modules=find_py_modules(),
    install_requires=[],    # install_requires字段可以列出依赖的包信息，用户使用pip或easy_install安装时会自动下载依赖的包
    author='jianzhong.zhou',
    url='https://github.com',
    author_email='1329870572@qq.com',
    license='MIT',
    # packages=find_packages(),   # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    packages=['excel_convert_xml'],   # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    zip_safe=True,
    include_package_data=True,

    package_data={
        'excel_convert_xml': ['config.ini', 'IHG-SchedulerTestCase.xls', 'upload pypi.txt']
    },

    # data_files=data_files,
    # package_dir={'OnePiece': 'jar'},
)

"""1. 在包的同級目錄下添加setup.py 的文件，詳情見setup.py 文件
2. 配置相應的包或者模塊
3. 在setup.py 的當前路徑執行以下命令：
3.1、 python setup.py build (在當前路徑會出現build的文件夾./build/lib/包名)
3.2、 打包方式有兩種：
3.2.1、python setup.py sdist (在當前路徑下會生成dist的文件夾./dist;
打成了zip後綴的文件，如果要打成其它格式，執行 python setup.py --help )
3.2.2、 python setup.py bdist_wheel(如果報錯，看有沒有安裝wheel,pip install wheel
在當前路徑下會生成dist文件夾，文件夾中的文件是以包名+版本號**.whl)
例子：[OnePiece-1.0.0-py2-none-any.whl]

4. 上傳到pypi
4.1、到 https://testpypi.python.org/pypi/ 註冊賬號
4.2、在系統當前賬號下創建：.pypirc的文件， 記得後面 ：.pypirc加"."。
4.3、文件配置見文件
4.4、 注册你的包注册的方式有以下2种：
4.4.1、python setup.py register，最简单但官网不推荐，因为使用的是HTTP未加密，
有可能会被攻击人嗅探到你的密码。通过PyPI网站提交表单完成注册验证。
4.4.2、pip install twine；然后在通过命令 twine register dist/mypkg.whl 完成注册。
注册时cmd内容：
C:\Users\xxx>python D:\python\interface_demo\setup.py register
running register
running egg_info
creating interface_demo.egg-info
writing interface_demo.egg-info\PKG-INFO
writing top-level names to interface_demo.egg-info\top_level.txt
writing dependency_links to interface_demo.egg-info\dependency_links.txt
writing manifest file 'interface_demo.egg-info\SOURCES.txt'
warning: manifest_maker: standard file 'setup.py' not found
reading manifest file 'interface_demo.egg-info\SOURCES.txt'
writing manifest file 'interface_demo.egg-info\SOURCES.txt'
running check
We need to know who you are, so please choose either:
1. use your existing login,
2. register as a new user,
3. have the server generate a new password for you (and email it to you), or
4. quit
Your selection [default 1]： 1
Username: xxxx
Password:
Registering interface_demo to https://upload.pypi.org/legacy/
Server response (410): Project pre-registration is no longer required or supported, so continue directly to uploading files.

4.5、上传并完成发布：以下两种方式之
4.5.1、python setup.py sdist upload，还是和上面一样，最简单但是有安全隐患。

4.5.2、使用 twine： twine upload dist/*

上传成功cmd内容：
C:\Users\xxxx>python D:\python\interface_demo\setup.py sdist upload
running sdist
running egg_info
writing interface_demo.egg-info\PKG-INFO
writing top-level names to interface_demo.egg-info\top_level.txt
writing dependency_links to interface_demo.egg-info\dependency_links.txt
warning: manifest_maker: standard file 'setup.py' not found
reading manifest file 'interface_demo.egg-info\SOURCES.txt'
writing manifest file 'interface_demo.egg-info\SOURCES.txt'
warning: sdist: standard file not found: should have one of README, README.rst, README.txt
running check
creating interface_demo-1.0.0
creating interface_demo-1.0.0\interface_demo.egg-info
copying files to interface_demo-1.0.0...
copying interface_demo.egg-info\PKG-INFO -> interface_demo-1.0.0\interface_demo.egg-info
copying interface_demo.egg-info\SOURCES.txt -> interface_demo-1.0.0\interface_demo.egg-info
copying interface_demo.egg-info\dependency_links.txt -> interface_demo-1.0.0\interface_demo.egg-info
copying interface_demo.egg-info\top_level.txt -> interface_demo-1.0.0\interface_demo.egg-info
copying interface_demo.egg-info\zip-safe -> interface_demo-1.0.0\interface_demo.egg-info
Writing interface_demo-1.0.0\setup.cfg
Creating tar archive
removing 'interface_demo-1.0.0' (and everything under it)
running upload
Submitting dist\interface_demo-1.0.0.tar.gz to https://upload.pypi.org/legacy/
Server response (200): OK
4.6、 檢查包是否上傳到pipy, 闊以根據上傳的結果看，還闊以登入到遠程看上面是否已經顯示上傳的包































"""




















