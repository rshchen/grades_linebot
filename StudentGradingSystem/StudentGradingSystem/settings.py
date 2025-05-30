"""
Django settings for StudentGradingSystem project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'kghsgrades.blesstw.com',  # 添加你的域名
    'samplescores.blesstw.com',
    'c275-219-69-66-52.ngrok-free.app', #ngrok測試用
]


CSRF_TRUSTED_ORIGINS = [
    'https://kghsgrades.blesstw.com',
    'https://samplescores.blesstw.com',
    'https://c275-219-69-66-52.ngrok-free.app', #ngrok測試用
]

# 網站的基 URL
SITE_URL = 'https://c275-219-69-66-52.ngrok-free.app'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'grades',  # 你的應用
    
    # 管理allauth套件及所需新增的程式碼
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Google OAuth
    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # 新增這一行
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'StudentGradingSystem.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'grades', 'templates')],  # 新增這一行
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

WSGI_APPLICATION = 'StudentGradingSystem.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'zh-hant'  # 使用繁體中文
# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# 這些設置允許使用者在網站上切換語言
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 設置可用的語言列表
LANGUAGES = [
    ('zh-hant', '繁體中文'),
    ('en', 'English'),
    # 可以添加更多語言
]

# 添加以下行以加載翻譯文件
LOCALE_PATHS = [
    BASE_DIR / 'locale',  # 根據你的專案結構調整
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# 靜態文件的 URL 前綴
STATIC_URL = '/static/'

# 靜態文件的目錄
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # 你的靜態文件目錄
]

# 靜態文件的收集目錄（用於生產環境）
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allauth 設定
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Google OAuth 設定
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
#ACCOUNT_EMAIL_VERIFICATION = False  # 或者設為 False
#ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True  # 使得登錄後能夠自動重定向
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # 強制要求電子郵件驗證
#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')




# 電子郵件驗證設定
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # 或者你的SMTP伺服器
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')

# 添加 Allauth 的 SocialAccount Provider 設置
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'),
            'secret': config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'),
            'key': ''
        },
        'AUTH_PARAMS': {
            'prompt': 'select_account'  # 確保每次登入時選擇帳號
        },
    }
}



# 日誌檢查
#import os
#
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'formatters': {
#        'verbose': {
#            'format': '{levelname} {asctime} {module} {message}',
#            'style': '{',
#        },
#        'simple': {
#            'format': '{levelname} {message}',
#            'style': '{',
#        },
#    },
#    'handlers': {
#        'file': {
#            'level': 'DEBUG',
#            'class': 'logging.FileHandler',
#            'filename': os.path.join(BASE_DIR, 'django_debug.log'),  # 將日誌寫入到檔案
#            'formatter': 'verbose',
#        },
#        'console': {
#            'class': 'logging.StreamHandler',
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers': ['file', 'console'],  # 同時將日誌輸出到檔案和控制台
#            'level': 'DEBUG',
#            'propagate': True,
#        },
#        'linebot': {  # 為 LINE bot 自定義 logger
#            'handlers': ['file'],
#            'level': 'DEBUG',
#            'propagate': True,
#        },
#    },
#}
