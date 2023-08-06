# 配置文件
import os
import sys

# 设置工程的source root 目录位置，默认是项目的根路径
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'BruceSky'))

project_name = 'BruceSky'

icon = r'firelaunching/favicon.ico'

protocol = ['UDP', 'TCP']
