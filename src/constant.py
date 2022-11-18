"""
Name         : 基础常量
Version      : 1.0.1
Author       : zzz
Date         : 2022-01-11 12:13:42
LastEditors  : zzz
LastEditTime : 2022-10-21 12:59:37
"""
import os
import yaml

# 项目根目录
_project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库文件地址
DB_DIR = os.path.join(_project_path, "db")
SQLITE3_FILE = os.path.join(DB_DIR, "db.sqlite3")

# 日志文件地址
LOG_DIR = os.path.join(_project_path, "log")

# 其他文件地址
DOC_DIR = os.path.join(_project_path, "doc")

# 项目配置文件地址
_conf_path = os.path.join(_project_path, "conf.yaml")

# 读取项目设置
with open(_conf_path, "r", encoding="utf-8") as f:
    conf = yaml.load(f.read(), Loader=yaml.FullLoader)
