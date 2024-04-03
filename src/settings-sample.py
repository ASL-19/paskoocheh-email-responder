# coding=UTF8
"""
Settings file for email responder
"""
import logging
import os
# __file__ refers to the file settings.py
CONFIG = {
    'LANG': 'fa',
    'VERSION': '3.0.0',
    # refers to application_top
    'APP_PATH': os.path.dirname(os.path.abspath(__file__)),
    'MAX_ATTACHMENT_SIZE': 500000,    # max size in bytes of attachment
    'IS_DEBUG': '$IS_DEBUG',
    # 'LOG_LEVEL': logging.INFO,
    'APPLICATION_SOURCE': {
        'en': 'Paskoocheh Email Bot',
        'fa': 'Paskoocheh Email Bot',
        'ar': 'Mada19 Email Bot'
    },
    'CONFIDENTIAL_ACCESS': 'conf_access.json',

    'CONF_S3_BUCKET': '$CONF_S3_BUCKET',
    'FILE_S3_BUCKET': '$FILE_S3_BUCKET',
    'CONF_S3_KEY': 'config/apps.json',
    'NEWS_BUCKET': '$NEWS_BUCKET',
    'NEWS_FILENAME': 'emrooz_body.html',
    'START_EMAIL': '$START_EMAIL',
    'NEWS_EMAIL': '$NEWS_EMAIL',
    'REPLY_EMAIL': {
        'en': '$REPLY_EMAIL_EN',
        'fa': '$REPLY_EMAIL_FA',
        'ar': '$REPLY_EMAIL_AR'
    },
    'FEEDBACK_EMAIL': '$FEEDBACK_EMAIL',
    'OUTLINE_EMAIL': '$OUTLINE_EMAIL',
    'TG_PROXY_EMAIL': '$TG_PROXY_EMAIL',

    'SOS_EMAIL': '$SOS_EMAIL',
    'SOS_FILE': 'rescue_package.pdf',

    "PROMO_CODE_EXPIRY_DATE": "۱۴۰۲/۰۶/۱۹",
    "PROMO_CODE_RECIPIENTS": [
        'mullvad-android@paskoocheh.com',
        'mullvad-windows@paskoocheh.com',
        'mullvad-macos@paskoocheh.com',
        'mullvad-linux@paskoocheh.com'
    ],
    "PROMO_EXPIRY": 2592000,
    "DOWNLOAD_EXPIRY": 86400,
    "S3_PROMO_BUCKET_NAME": "$S3_PROMO_BUCKET_NAME",
    "S3_PROMO_FILE_EXTENSION": ".promo",
    "S3_PROMO_FILE_EXTENSION_TEST": ".txt",
    "S3_KEY_BUCKET_NAME": "$S3_KEY_BUCKET_NAME",
    "S3_KEY_FILE_EXTENSION": ".key",

    "S3_SSCONFIG_BUCKET_NAME": "$S3_SSCONFIG_BUCKET_NAME",
    "S3_SSCONFIG_MAX_AGE": "$S3_SSCONFIG_MAX_AGE",

    'S3_PROXY_BUCKET': '$S3_PROXY_BUCKET',
    'MTPROTO_PROXY_FILE': 'mtproxy.json',
    'TELEGRAM_WEBSITE_SHORTLINK': 'https://t.me',
    'OUTLINE_AWS_URL': 'https://s3.amazonaws.com/$OUTLINE_INVITATION_BUCKET/invite.html#%s',
    "OUTLINE_CONFIG_AWS_URL": "https://s3.amazonaws.com/$OUTLINE_INVITATION_BUCKET/fa/start.html?key=%s",
    'OUTLINE_PROJECTS': {
        'syriaonline': 'syriaonline',
        'syria online': 'syriaonline'
    }
}
