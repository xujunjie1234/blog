import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# print(os.path.dirname(__file__))
# print(os.path.dirname(os.path.dirname(__file__)))
# print(basedir)


class BaseConfig:
    #密钥
    SECRET_KEY = os.getenv('SECRET_KEY', "secret key")
    
    #测试
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_ALLOW_ALL = True
    

    #数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    #使返回的json数据正确显示中文
    JSON_AS_ASCII = False

    #允许图片格式
    MYBLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

    #头像图片储存路径
    AVATAR_PATH = os.path.join(basedir,'uploads//avatar')



class DevelopmentConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/blog"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    TESTING = True
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestConfig
}