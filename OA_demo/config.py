"""
配置文件
所有的配置都在这里
"""

SECRET_KEY = 'jkahdaklfshlk;afsj'

# 数据库的配置信息
HOSTNAME = '127.0.0.1'
PORT = 3306
DATABASE = 'oasql_demo'
USERNAME = 'root'
PASSWORD = '123456'
# DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URL
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2147536132@qq.com"
MAIL_PASSWORD = "bfuamkssghkceafa"
MAIL_DEFAULT_SENDER = "2147536132@qq.com"

