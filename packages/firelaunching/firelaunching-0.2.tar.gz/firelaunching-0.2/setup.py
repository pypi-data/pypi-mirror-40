from os.path import dirname, join
from setuptools import setup, find_packages

with open(join(dirname(__file__), 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name="firelaunching",  # pypi中的名称，pip或者easy_install安装时使用的名称
    version=version,  # (-V) 包版本
    author="Bruce Yu",  # 程序的作者
    author_email="991138518@qq.com",  # 程序的作者的邮箱地址
    description="This is a service of send messages",  # 程序的简单描述
    long_description=open('README.md', encoding='utf-8').read(),  # 程序的详细描述
    license="BSD",  # 程序的授权信息
    keywords="ftp udp",  # 程序的关键字列表
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    include_package_data=True,
    data_files=["firelaunching/favicon.ico"],
    packages=find_packages(exclude=('tests', 'tests.*')),
    py_modules=["FireLaunching"],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'wxPython>=4.0.3',
        'chardet>=3.0.4',
    ],

    classifiers=[
        # 'Development Status :: 1-Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],

    entry_points={
        'console_scripts': [
            'firelaunching = FireLaunching:main',
        ]
    }

)
