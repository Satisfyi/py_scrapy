"""
Django 项目配置文件

对于初学者来说，你只需要关注这几个配置：
1. INSTALLED_APPS  - 告诉 Django 有哪些功能模块
"""

from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥（开发用，生产环境需要换）
SECRET_KEY = 'django-insecure-#%nut4+os)93paf0htw)bz871_$0z+t9mjveq#7k^#9ns9z@mi'

# 开启调试模式（开发时必须为 True，可以看到详细错误信息）
DEBUG = True

# 允许所有主机访问（开发阶段无所谓）
ALLOWED_HOSTS = ['*']


# ================================================================
# 应用注册
# 告诉 Django：「我要用这些功能」
# ================================================================

INSTALLED_APPS = [
    'django.contrib.admin',         # 后台管理系统
    'django.contrib.auth',          # 用户认证（登录/注册）
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   # 静态文件（CSS/JS/图片）

    # ---- 我们自己的应用 ----
    'topics',                       # 知乎热榜应用
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zhihu_project.urls'


# 模板配置
# DIRS：告诉 Django 去 templates/ 文件夹找 HTML 文件

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],    # ← 我们的 HTML 放这里
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zhihu_project.wsgi.application'


#数据库连接
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zhihu',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'127.0.0.1',
        'port':3306
    }
}


# 密码验证（使用默认的就行）
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


#时区和语言
LANGUAGE_CODE = 'zh-hans'          # 中文
TIME_ZONE = 'Asia/Shanghai'        # 北京时间
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ================================================================
# 静态文件
# 我们的 CSS 放在 static/ 文件夹
# ================================================================

STATIC_URL = '/static/'

# 告诉 Django 在项目根目录的 static/ 找静态文件
STATICFILES_DIRS = [
    BASE_DIR / 'templates' / 'static',
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
