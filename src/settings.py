# coding=UTF8
"""
Settings file for email responder
"""
import logging
import os
# __file__ refers to the file settings.py
CONFIG = {
    'LANG': 'fa',
    'APP_PATH': os.path.dirname(os.path.abspath(__file__)),   # refers to application_top
    'MAX_ATTACHMENT_SIZE': 7500000,    # max size in bytes of attachment
    'LOG_LEVEL': logging.INFO,
    'SOURCE_APP': '',
    'API_KEY_ID': '',
    'SECRET_KEY': '',
    'CONF_S3_BUCKET': '',
    'CONF_S3_KEY': '',
    'NEWS_BUCKET': '',
    'NEWS_FILENAME': '',
    'START_EMAIL': '',
    'NEWS_EMAIL': '',
    'REPLY_EMAIL': '',
    'FEEDBACK_EMAIL': '',
    'EMAIL_SUBJECT': '',
    'TEMPLATES': {
        'TEXT_BODY': {
            'en': """
            """,
            'fa': """
            """,
            'ar': """
            """
        },
        'HTML_BODY': {
            'en': """
            """,
            'fa': """
            """,
            'ar': """
            """
        },
        'WIN_TEXT_BODY': {
            'en': """
            """,
            'fa': """
            """,
            'ar': """
            """
        },
        'WIN_HTML_BODY': {
            'en': """
            """,
            'fa': """
            """,
            'ar': """
            """
        },
        'ATTACHMENT_HTML': {
            'en': """
            """,
            'fa': """
            """,
            'ar': """
            """
        },
        'BIA_TEXT': {
            'en': """
            """,
            'fa': """
            """,
            'ar': """
            """
        },
        'BIA_HTML': {
            'en': """
            """,
            'fa': """
            """,
            'ar': """
            """
        }
    }
}
