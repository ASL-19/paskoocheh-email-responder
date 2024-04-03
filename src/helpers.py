# Copyright 2020 ASL19 Organization
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import json
import random
import hashlib
import re
import requests
import base64
from datetime import datetime
from os import path
from botocore.config import Config
from botocore.exceptions import ClientError
import boto3
from translation import Translation
from settings import CONFIG
from templates import TEMPLATES
from pyskoocheh import feedback
from pyskoocheh.log import get_logger
from pyskoocheh.errors import ValidationError
from pyskoocheh import (
    actionlog,
    storage,
    telegram,
    database,
    dbconnect,
    util
)
import globalvars
if sys.version_info[0] == 2:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse


logger = get_logger('EmailResponder', __name__)


def change_lang(new_lang):
    """
    Change language of the user and apply the required changes

    :param new_lang: New language to be stored
    """
    try:
        globalvars.lang = Translation(new_lang, CONFIG['LANGUAGE_FILE'])
    except Exception as exc:
        logger.error(f"Error in Language file: {exc}")
        raise

    globalvars.HOME_KEYBOARD = [
        [
            globalvars.lang.text('MENU_OS_TEXT'),
            globalvars.lang.text('MENU_APP_TEXT')
        ],
        [
            globalvars.lang.text('MENU_SIGNAL_PROXY'),
            globalvars.lang.text('MENU_RESCUE_PACKAGE')
        ],
        [
            globalvars.lang.text('MENU_PASK_APK'),
            globalvars.lang.text('MENU_TELEGRAM_PROXY')
        ],
        [
            globalvars.lang.text('MENU_CHANGE_LANGUAGE'),
            globalvars.lang.text('MENU_FEEDBACK')
        ],
        [
            globalvars.lang.text('MENU_OUTLINE'),
            globalvars.lang.text('MENU_MAILING_LIST')
        ]
    ]

    globalvars.OPT_IN_KEYBOARDS = [
        [
            globalvars.lang.text('OPT_IN_KEYBOARD'),
            globalvars.lang.text('OPT_OUT_KEYBOARD')
        ]
    ]

    globalvars.OLD_OR_NEW_SSLINK = [
        [
            globalvars.lang.text('GET_OLD_SSLINK'),
            globalvars.lang.text('GET_NEW_SSLINK')
        ]
    ]

    globalvars.USER_OUTLINE_REPORT = [
        [
            globalvars.lang.text('SERVER_BLOCKED_CASE_1'),
            globalvars.lang.text('SERVER_BLOCKED_CASE_2')
        ],
        [
            globalvars.lang.text('SERVER_BLOCKED_CASE_3'),
            globalvars.lang.text('SERVER_BLOCKED_CASE_4')
        ]
    ]

    globalvars.OUTLINE_SERVER_ISSUES = [
        globalvars.lang.text("SERVER_BLOCKED_CASE_1"),
        globalvars.lang.text("SERVER_BLOCKED_CASE_2"),
        globalvars.lang.text("SERVER_BLOCKED_CASE_3"),
        globalvars.lang.text("SERVER_BLOCKED_CASE_4"),
    ]


def make_pkg_name(app, platform):
    '''
        Create pkg_name using app name and platform

        Args:
        app: app name
        platform: platform for the app

        Returns:
        name to be used as pkg name for database
    '''

    pkg = app + '_' + platform
    pkg = re.sub(r'\W+', '', pkg.lower())

    return pkg


def get_db_connection(db_name='TELEGRAM_DB'):
    with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
        conf_access = json.load(conf_sec)
        try:
            if globalvars.RDS_IS_MYSQL:
                db_connection = dbconnect.mysql_connect(conf_access[db_name])
            else:
                db_connection = dbconnect.psql_connect(conf_access[db_name])

        except Exception as exc:
            logger.error('Error while creating a db connection ({})'.format(str(exc)))
            raise
    return db_connection


def save_chat_state(user_id, chat_id, state, user_info, extra_info=None):
    """
        Save chat state

        Args:
        user_id: Chat user ID
        chat_id: Telegram Chat ID
        state: User Chat State
        user_info: Other User information
        extra_info: Information to be annexed to the state
        for later retrieval

        Returns:
        True in case of success and False otherwise
    """

    data = {
        'user_uuid': user_id,
        'chat_id': chat_id,
        'state': state,
        'user_info': user_info,
        'extra_info': extra_info
    }
    try:
        conn = get_db_connection()
        database.save_chat_state(data, conn, globalvars.RDS_IS_MYSQL)
    except Exception as exc:
        logger.error(CONFIG['TELEGRAM_DB_ERR'].format(str(exc)))


def get_user_language(user_id):
    """
        Get preferred language for the user

        Args:
        user_id: Chat user ID

        Returns:
        Language code or None if user is not found
    """

    try:
        conn = get_db_connection()
        language = database.get_user_language(user_id, conn)
    except Exception as exc:
        logger.error('Error reading from user_lang db {}'.format(str(exc)))
        return None

    return language


def save_user_language(user_id, language):
    """
        Save preferred language for the user

        Args:
        user_id: Chat user ID
        language: Preferred language

        Returns:
        Language code or None if user is not found
    """

    data = {
        'user_uuid': user_id,
        'language': language,
    }

    try:
        conn = get_db_connection()
        language = database.save_user_language(data, conn, globalvars.RDS_IS_MYSQL)
    except Exception as exc:
        logger.error(
            CONFIG['TELEGRAM_DB_ERR'].format(str(exc)))


def make_combination_name(app_name, os_name):
    """
        Makes the text to send as Application + OS
        to show as a keyboard button

        Args:
        app: app name
        os: OS the app is written for

        Returns:
        App + OS name for messages
    """

    return app_name + ' - ' + os_name


def parse_conf_data(apps, gnt, dnr):
    """
        Parses the configuration data and creates the
        dictionary of apps and OSes to show to the user

        Args:
        apps: the configuration json for apps
        gnt: guides and tutorials information json file
        dnr: download and rating information json file
    """

    if not apps:
        logger.error('Configuration file is empty')
        return

    for cat in apps['categories']:
        cat_name = cat['name']['fa']
        globalvars.categorylist[str(cat['id'])] = {
            'name': cat_name
        }

    tools = {}
    for tool in apps['tools']:
        tools[tool['name']] = {
            'info': tool['info']
        }

    tutes = {}
    if gnt is not None:
        for osname, os in gnt['versions'].items():
            for ver in os:
                ver_name = make_combination_name(ver['app_name'], osname)
                tutes[ver_name] = ver['tutorial']

    dnr_vals = {}
    if dnr is not None:
        for obj in dnr:
            ver_name = make_combination_name(
                obj['tool_name'], obj['platform_name'])
            dnr_vals[ver_name] = {
                'downloads': obj['download_count'],
                'rating': obj['rating'],
                'rating_count': obj['rating_count']
            }

    for platform in apps['versions']:

        name = platform
        if name not in globalvars.oslist:
            globalvars.oslist.append(name)
            globalvars.applistos[name] = []

        for tool in apps['versions'][platform]:
            toolName = tool['app_name']

            if toolName not in globalvars.namelist:
                globalvars.namelist.append(toolName)
                globalvars.applistname[toolName] = []

            ver_name = make_combination_name(toolName, name)

            for cat in tool['categories']:
                cat_name = globalvars.categorylist[cat]['name']
                if platform not in globalvars.toolcat:
                    globalvars.toolcat[platform] = {}
                if cat_name not in globalvars.toolcat[platform]:
                    globalvars.toolcat[platform][cat_name] = []
                globalvars.toolcat[platform][cat_name].append(ver_name)
                catosname = make_combination_name(cat_name, platform)
                if catosname not in globalvars.catoslist:
                    globalvars.catoslist[catosname] = []
                if ver_name not in globalvars.catoslist[catosname]:
                    globalvars.catoslist[catosname].append(ver_name)

            if ver_name not in globalvars.apposlist:
                globalvars.apposlist[ver_name] = {
                    'app': toolName,
                    'tool_id': tool['tool_id'],
                    'version': tool['version_number'],
                    'release_date': tool['release_date'],
                    'size': int(tool['size'])/1024,
                    'os': name,
                    'key': tool['s3_key'],
                    'desc': tools[toolName]['info'],
                    'faq_url': tool['faq_url'],
                    'guide_url': tool['guide_url'],
                    'tut': tutes[ver_name] if ver_name in tutes else None,
                    'dnr': dnr_vals[ver_name] if ver_name in dnr_vals else None,
                    'filename': path.basename(str(urlparse(tool['download_via']['url']))),
                    'release_url': tool['download_via']['url'],
                    'action_name': re.sub(r'[^a-z0-9]+', '', toolName.lower()) + '-' + name.lower()
                }
            if toolName not in globalvars.applistos[name]:
                globalvars.applistos[name].append(toolName)
            if name not in globalvars.applistname[toolName]:
                globalvars.applistname[toolName].append(name)
        logger.debug(f"OS List: {globalvars.oslist}")


def send_file_or_link(token, chat_id, key, url, action_name, values, extra_msg=''):
    """
        Send the file pointed to by key to the user if
        it's smaller than less allowed size, or the link
        otherwise.

        Args:
        token: Telegram Bot token
        chat_id: Telegram Chat ID
        key: The file on S3
        url: release url, used if there is no key
        action_name: Name of the file to store in db
        extra_msg: If provided it sends the message to the user
    """

    logger.debug('Sending file {}'.format(key))

    channel_name = globalvars.lang.text('TELEGRAM_BOT_NAME')  # type: ignore

    if not key or key == '':
        meta = {
            'content_length': CONFIG['MAX_ALLOWED_FILE_SIZE']
        }
        telegram.send_message(token, chat_id, globalvars.lang.text(  # type: ignore
            'MSG_FILE_DOWNLOAD') + '\n' + url, [[url]])

    else:
        try:
            link = storage.build_static_link(CONFIG['S3_BUCKET_NAME'], key)

        except Exception as e:
            logger.error('Unable to get the link (bucket={}, key={}) error ({})'.format(
                CONFIG['S3_BUCKET_NAME'], key, str(e)))
            telegram.send_message(
                token, chat_id, globalvars.lang.text('MSG_FAILED_DOWNLOAD'))  # type: ignore
            return

        try:
            meta = storage.get_object_metadata(CONFIG['S3_BUCKET_NAME'], key)

        except Exception as e:
            logger.error('Unable to get the metadata (bucket={}, key={}) error ({})'.format(
                CONFIG['S3_BUCKET_NAME'], key, str(e)))
            telegram.send_message(
                token, chat_id, globalvars.lang.text('MSG_FAILED_DOWNLOAD'))  # type: ignore
            return

        logger.debug('Checking file size')

        if meta.content_length < CONFIG['MAX_ALLOWED_FILE_SIZE']:
            logger.debug('Uploading File')
            telegram.send_message(token, chat_id, globalvars.lang.text('MSG_WAIT'))  # type: ignore

            if extra_msg != '':
                telegram.send_message(token, chat_id, extra_msg)

            n = random.randint(0, 99)
            logger.debug("NUMBER IS {}".format(str(n)))
            if n < CONFIG['CENO']:
                logger.debug('SENDING THROUGH CENO')
                try:
                    with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
                        conf_access = json.load(conf_sec)
                        proxies = {
                            'http': 'http://{USER}:{PASSWORD}@{INJECTOR_ADDRESS}'.format(
                                USER=conf_access['CENO_CONFIG']['PROXY_USER'],
                                PASSWORD=conf_access['CENO_CONFIG']['PROXY_PASS'],
                                INJECTOR_ADDRESS=conf_access['CENO_CONFIG']['PROXY_TCP_ADDRESS']),
                            'https': 'http://{USER}:{PASSWORD}@{INJECTOR_ADDRESS}'.format(
                                USER=conf_access['CENO_CONFIG']['PROXY_USER'],
                                PASSWORD=conf_access['CENO_CONFIG']['PROXY_PASS'],
                                INJECTOR_ADDRESS=conf_access['CENO_CONFIG']['PROXY_TCP_ADDRESS'])
                        }
                        logger.debug('CeNo Config is {}'.format(proxies))
                        telegram.send_file(token, chat_id, globalvars.lang.text(  # type: ignore
                            'MSG_FILE_DOWNLOAD') + '\n' + link, CONFIG['S3_BUCKET_NAME'], key, Config(proxies=proxies))
                        channel_name = globalvars.lang.text('TELEGRAM_BOT_NAME') + '_ceno'  # type: ignore
                except Exception as exc:
                    logger.error('Error getting file from CeNo {}'.format(exc))
                    telegram.send_file(token, chat_id, globalvars.lang.text(  # type: ignore
                        'MSG_FILE_DOWNLOAD') + '\n' + link, CONFIG['S3_BUCKET_NAME'], key)
            else:
                telegram.send_file(token, chat_id, globalvars.lang.text(  # type: ignore
                    'MSG_FILE_DOWNLOAD') + '\n' + link, CONFIG['S3_BUCKET_NAME'], key)

        else:
            logger.debug('File too large, sending link')
            with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
                conf_access = json.load(conf_sec)

            api_key_id = conf_access['LIMITED_ACCESS']['API_KEY_ID']
            secret_key = conf_access['LIMITED_ACCESS']['SECRET_KEY']
            temp_link = storage.get_temp_link(
                CONFIG['S3_BUCKET_NAME'], key, api_key_id, secret_key)
            telegram.send_message(token, chat_id, globalvars.lang.text(  # type: ignore
                'MSG_FILE_DOWNLOAD') + '\n' + temp_link, [[temp_link]])
            telegram.send_message(token, chat_id, globalvars.lang.text('TEMP_LINK_TEXT'))  # type: ignore

    logger.debug('{} is added to the db'.format(action_name))

    data = {
        'user_uuid': str(chat_id),
        'tool': values['app'],
        'channel': channel_name,
        'platform': values['os'],
        'tool_version': values['version'],
        'platform_version': None,
        'download_time': None,
        'downloaded_via': 's3' if key else 'url',
        'country': None,
        'city': None,
        'network_type': None,
        'file_size': values['size'],
        'network_name': None,
        'channel_version': CONFIG['VERSION'],
        'network_country': None,
        'timezone': None,
        'tool_id': values['tool_id']
    }

    try:
        conn = get_db_connection('STATS_DB')
        database.write_download(data, conn)
    except Exception as exc:
        logger.error(f"Error while storing STATS: {exc}")


def get_key_code(tool):
    """
        Look for key codes and if there is any
        returns it to the user.
        Key codes are reusable code that we can send to more
        than one user. The selection of key code to send to a
        user is random.

        Args:
        tool: Tool name to look for key

        Returns:
        A tuple consisting of:
            A string containing key code or empty if there is none and a guide link
            Link to key guide
    """

    key_name = re.sub('\s+', '', tool).lower().strip() + \
        CONFIG['S3_KEY_FILE_EXTENSION']

    logger.debug('Checking S3 for Key codes for {}'.format(key_name))

    with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
        conf_access = json.load(conf_sec)

    try:
        pfile = storage.get_file_with_creds(
            CONFIG['S3_KEY_BUCKET_NAME'],
            key_name,
            conf_access['KEY_ACCESS']['ACCESS_KEY'],
            conf_access['KEY_ACCESS']['SECRET_KEY'])
    except Exception as e:
        if "NoSuchKey" in str(e):
            logger.info('Unable to get key file from S3: {}'.format(str(e)))
        else:
            logger.error('Unable to get key file from S3: {}'.format(str(e)))
        return '', ''

    if not pfile or 'Body' not in pfile:
        return '', ''

    try:
        codes = json.load(pfile['Body'])

    except Exception as e:
        logger.error('Error in json file {} form {} due to {}: {}'.format(
            key_name,
            CONFIG['S3_KEY_BUCKET_NAME'],
            str(e),
            pfile['Body']))
        return '', ''

    logger.debug('File found: {}'.format(str(codes)))
    if 'keys' not in codes or len(codes['keys']) == 0:
        return '', ''

    n = random.randint(0, len(codes['keys'])-1)
    key = codes['keys'][n]['key']
    link = codes['keys'][n]['link']

    logger.debug('Code found: {} {}'.format(str(link), str(key)))
    return key, link


def return_promo_code_file(key_name):
    """
        check if promo code file exist
        Args:
        tool: Tool name to look for promo

        Returns:
        A tuple consisting of:
            A string containing promo code or empty if there is none and a guide link
            Link to Promo guide
    """
    with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
        conf_access = json.load(conf_sec)

    try:
        pfile = storage.get_file_with_creds(
            CONFIG['S3_PROMO_BUCKET_NAME'],
            key_name,
            conf_access['PROMO_ACCESS']['ACCESS_KEY'],
            conf_access['PROMO_ACCESS']['SECRET_KEY'])
    except Exception as e:
        if "NoSuchKey" in str(e):
            logger.info('Unable to get promo file from S3: {}'.format(str(e)))
        else:
            logger.error('Unable to get promo file from S3: {}'.format(str(e)))
        return '', ''

    if not pfile or 'Body' not in pfile:
        return '', ''
    logger.debug('this is the body \n {}'.format(pfile['Body']))

    return pfile


def get_promo_code(values, user_id):
    """
        Look for promo codes and if there is any
        returns it to the user.

        Args:
        tool: Tool name to look for promo

        Returns:
        A tuple consisting of:
            A string containing promo code or empty if there is none and a guide link
            Link to Promo guide
    """

    key_name = re.sub(
        '\s+', '', values['app']).lower().strip() + CONFIG['S3_PROMO_FILE_EXTENSION']

    logger.debug('Checking S3 for Promo codes for {}'.format(key_name))

    channel_name = 'EMAIL_RESPONDER'

    logger.debug('Checking S3 for Promo codes for {}'.format(key_name))

    with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
        conf_access = json.load(conf_sec)

    try:
        pfile = storage.get_file_with_creds(
            CONFIG['S3_PROMO_BUCKET_NAME'],
            key_name,
            conf_access['PROMO_ACCESS']['ACCESS_KEY'],
            conf_access['PROMO_ACCESS']['SECRET_KEY'])
    except Exception as e:
        if "NoSuchKey" in str(e):
            logger.info('Unable to get promo file from S3: {}'.format(str(e)))
        else:
            logger.error('Unable to get promo file from S3: {}'.format(str(e)))
        return '', ''

    if not pfile or 'Body' not in pfile:
        return '', ''

    try:

        codes = json.load(pfile['Body'])

    except Exception as e:
        logger.error('Error in json file {} form {} due to {}: {}'.format(
            key_name,
            CONFIG['S3_PROMO_BUCKET_NAME'],
            str(e),
            pfile['Body']))
        return '', ''

    logger.debug('File found: {}'.format(str(codes)))
    if 'unused' not in codes or len(codes['unused']) == 0:
        return '', ''

    code = codes['unused'].pop(0)
    if 'used' not in codes:
        codes[u'used'] = []
    codes[u'used'].append(code)

    link = ''
    if 'link' in codes:
        link = codes['link']

    data = {
        'user_uuid': str(user_id),
        'tool': values['app'],
        'channel': channel_name,
        'promo_code': str(code)
    }

    try:
        conn = get_db_connection('TELEGRAM_DB')
        database.write_promo_code(data, conn)
    except Exception as exc:
        logger.error(f"Error while storing PROMO CODE: {exc}")

    try:
        storage.put_file_with_creds(
            CONFIG['S3_PROMO_BUCKET_NAME'],
            key_name,
            json.dumps(codes),
            conf_access['PROMO_ACCESS']['ACCESS_KEY'],
            conf_access['PROMO_ACCESS']['SECRET_KEY'])

    except Exception as e:
        logger.error('Error in writing file {} form {} due to {}: {}'.format(
            key_name,
            CONFIG['S3_PROMO_BUCKET_NAME'],
            str(e),
            json.dumps(codes)))
        return '', ''

    logger.debug('File is written back')
    logger.debug("code {} and link --> {}".format(code, link))
    return code, link


def read_config_file(token, chat_id=0):
    """
        Parse Configuration Data for App and OS
    """

    try:
        stream = storage.get_binary_contents(
            CONFIG["S3_BUCKET_NAME"], CONFIG["S3_APPS_CONF_BUCKET_KEY"])['Body'].read()
        apps_file = json.loads(stream)
    except Exception as exc:
        logger.error('Error loading apps file from S3 ({})'.format(str(exc)))
        telegram.send_message(token, chat_id, globalvars.lang.text("MSG_ERROR"))  # type: ignore
        return None

    if not apps_file:
        telegram.send_message(token, chat_id, globalvars.lang.text("MSG_ERROR"))  # type: ignore
        return None

    try:
        stream = storage.get_binary_contents(
            CONFIG["S3_BUCKET_NAME"], CONFIG["S3_GNT_CONF_BUCKET_KEY"])['Body'].read()
        gnt_file = json.loads(stream)
    except Exception as exc:
        logger.error('Error loading gnt file from S3 ({})'.format(str(exc)))
        gnt_file = None

    try:
        stream = storage.get_binary_contents(
            CONFIG["S3_BUCKET_NAME"], CONFIG["S3_DNR_CONF_BUCKET_KEY"])['Body'].read()
        dnr_file = json.loads(stream)
    except Exception as exc:
        logger.error('Error loading dnr file from S3 ({})'.format(str(exc)))
        dnr_file = None

    return parse_conf_data(apps_file, gnt_file, dnr_file)


def record_exist(user_uuid, tool, platform, channel, table):

    if "promocode" in table:
        try:
            logger.debug("Looking at table {}".format(table))
            conn = get_db_connection('TELEGRAM_DB')
            expiry = CONFIG['PROMO_EXPIRY']
        except Exception as exc:
            logger.error(f"Error while creating DB connection to TELEGRAM_DB: {exc}")
            raise
    else:
        try:
            logger.debug("Looking at table {}".format(table))
            conn = get_db_connection('STATS_DB')
            expiry = CONFIG['DOWNLOAD_EXPIRY']
        except Exception as exc:
            logger.error(f"Error while creating DB connection to STATS_DB: {exc}")
            raise

    return database.record_exist(user_uuid, tool, platform, channel, conn, table, expiry)


def record_action(chat_id, msg):
    """
        Records the action in click stream data

        Args:
        chat_id: chat id with the user in order to be able to track the stream
        msg: msg sent by the user
    """

    try:
        actionlog.log_action(
            str(chat_id),
            msg,
            CONFIG["APPLICATION_SOURCE"],
            table=CONFIG["CLICKSTREAM_TABLE"])
    except:
        pass


def what_we_have(values):
    """
        Checks what information related to the current
        app we have and based on that we decide to show
        proper keyboard to the user

        Args:
        values: The dictionary containing all the properties for
        the app

        Returns:
        a dictionary mapping if we have FAQ, Tutorials or Guides
        for the selected app
    """

    wwh = {}

    wwh['faq'] = False
    if values['faq_url']:
        wwh['faq'] = True

    wwh['tut'] = False
    if values['tut'] and any(x in values['tut'] for x in ['video', 'video_link']):
        wwh['tut'] = True

    wwh['guide'] = False
    if values['guide_url']:
        wwh['guide'] = True

    return wwh


def make_dl_keyboard(wwh, msg):
    """
        A helper function to create download keyboard
        based on the information we have on the app

        Args:
        wwh: what we have dictionary that contains info on
        different attributes we have for the app
        msg: the text to be added to the various keys that
        represents the app

        Returns:
        A telegram keyboard containing relevant keys
    """

    sub_keyboard = [
        [
            globalvars.lang.text("MENU_RATING") + ": " + msg  # type: ignore
        ]
    ]

    sub_keyboard2 = []
    if wwh['faq']:
        sub_keyboard2.append(globalvars.lang.text("MENU_FAQ") + ": " + msg)  # type: ignore

    if wwh['tut']:
        sub_keyboard2.append(globalvars.lang.text("MENU_TUTORIAL") + ": " + msg)  # type: ignore

    if wwh['guide']:
        sub_keyboard2.append(globalvars.lang.text("MENU_GUIDE") + ": " + msg)  # type: ignore

    if len(sub_keyboard2) > 0:
        sub_keyboard.append(sub_keyboard2)

    sub_keyboard.append([globalvars.lang.text("HOME_TEXT")])  # type: ignore

    return sub_keyboard


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def base64_padding(txt):
    if len(txt) % 4:
        # not a multiple of 4, add padding:
        txt += '=' * (4 - len(txt) % 4)
    return txt


def find_proxy(user_id, filename):
    user_hash = int(hashlib.sha256(user_id.encode('utf-8')).hexdigest(), 16)

    with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
        conf_access = json.load(conf_sec)

        try:
            pfile = storage.get_file_with_creds(
                CONFIG['S3_PROXY_BUCKET'],
                filename,
                conf_access['PROXY_ACCESS']['ACCESS_KEY'],
                conf_access['PROXY_ACCESS']['SECRET_KEY'])
        except Exception as e:
            logger.error('Unable to get proxy file from S3: {}'.format(str(e)))
            raise ValueError('No Proxy')

        if not pfile or 'Body' not in pfile:
            raise ValueError('No Proxy')

        proxy_json = json.load(pfile['Body'])
        proxy_count = len(proxy_json['proxies'])
        n = user_hash % proxy_count

    return proxy_json['proxies'][n]


def find_wireguard_config(user_id):
    user_hash = hashlib.sha512(user_id.encode('utf-8')).hexdigest()
    logger.debug("inside the wireguard config finder")
    with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
        conf_access = json.load(conf_sec)

        try:
            pfile = storage.get_file_with_creds(
                CONFIG['S3_WIREGUARD_BUCKET'],
                CONFIG['WIREGUARD_CONFIG_LIST'],
                conf_access['WIREGUARD_ACCESS']['ACCESS_KEY'],
                conf_access['WIREGUARD_ACCESS']['SECRET_KEY'])
        except Exception as e:
            logger.error('Unable to get proxy file from S3: {}'.format(str(e)))
            return None, None

        if not pfile or 'Body' not in pfile:
            return None, None

        proxy_json = json.load(pfile['Body'])
        proxies = proxy_json[user_hash[0]]
        if len(proxies) > 1:
            n = random.randint(0, len(proxies)-1)
        else:
            n = 0
    conf_file = storage.get_file_with_creds(
        CONFIG['S3_WIREGUARD_BUCKET'],
        proxies[n],
        conf_access['WIREGUARD_ACCESS']['ACCESS_KEY'],
        conf_access['WIREGUARD_ACCESS']['SECRET_KEY'])

    return proxies[n], conf_file


def callback_query_request(tmsg):

    server, item, type = tmsg.body.split(',')
    if not server or not item:
        return False, None

    try:
        conn = get_db_connection('TELEGRAM_DB')
    except Exception as exc:
        logger.error(f"Error while creating DB connection to TELEGRAM_DB: {exc}")
        raise

    data = {
        'user_uuid': str(tmsg.user_id),
        'server': server,
        'item': item,
        'type': type
    }

    try:
        database.insert_into_callback(data, 'proxy_state', conn)
    except Exception as exc:
        logger.error(
            f'Error inserting callback_query {exc}')
        return False, None

    return True, globalvars.lang.text('RESP_THANKS_FOR_UPDATING')  # type: ignore


def update_ss_config(file_name, ss_link, ss_prefix=None):
    """
        Create or Update the SSconfig file
        returns the link from S3 bucket.

        Args:
        file_name: SSconfig file name, unique for each user

        Returns:
        A string containing S3 link to the SSconfig file
    """
    key_name = f'{file_name}.json'
    logger.debug(f'Updating {key_name} on S3 bucket')

    logger.debug(ss_link)
    ss_link = ss_link[5:].split("/")[0]
    ss_link = ss_link.split("@")
    ss_ip_port = ss_link[1].split(":")
    ss_decoded = base64.b64decode(base64_padding(ss_link[0]))
    ss_decoded = ss_decoded.decode("utf-8").split(":")
    ss_config_data = {
        "server": ss_ip_port[0],
        "server_port": ss_ip_port[1],
        "password": ss_decoded[1],
        "method": ss_decoded[0]
        }

    if ss_prefix:
        ss_config_data['prefix'] = ss_prefix

    with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
        conf_access = json.load(conf_sec)

    try:
        storage.put_file_with_creds(
            CONFIG['S3_SSCONFIG_BUCKET_NAME'],
            key_name,
            json.dumps(ss_config_data),
            conf_access['SSCONFIG_ACCESS']['ACCESS_KEY'],
            conf_access['SSCONFIG_ACCESS']['SECRET_KEY'],
            content_type="application/json",
            cache_control=f"max-age={CONFIG['S3_SSCONFIG_MAX_AGE']}")

    except Exception as e:
        logger.error('Error in writing file {} on {} due to {}'.format(
            key_name,
            CONFIG['S3_SSCONFIG_BUCKET_NAME'],
            str(e)))
        raise

    ss_config_link = "ssconf://s3.amazonaws.com/{}/{}".format(CONFIG['S3_SSCONFIG_BUCKET_NAME'], key_name)
    logger.debug(f'SSconfig json file is ready: {ss_config_link}')

    return ss_config_link


def inline_query_request(token, inline_query):
    """
        Handles inline query requests and returns
        the result for the query by searching
        the name of the apps and operating systems

        Args:
        token: Token of the bot
        inline_query: inline query submitted by the user
    """

    if inline_query['from']['is_bot']:
        return None

    query = inline_query['query'].lower()
    if len(query) < 3:
        return None

    offset = 0
    if 'offset' in inline_query and inline_query['offset']:
        logger.debug('Offset is {}'.format(inline_query['offset']))
        offset = int(inline_query['offset'])

    if any(pr in query for pr in ['proxy', 'proxies']):
        title = 'Telegram Proxy'
        url = 'https://telegram.me/PaskoochehBot?start={}'.format(
            base64.urlsafe_b64encode(globalvars.lang.text('MENU_TELEGRAM_PROXY').encode('utf-8')).decode('utf-8'))  # type: ignore
        answers = [{
            'type': 'article',
            'id': 1,
            'title': title,
            'url': url,
            'hide_url': True,
            'input_message_content': {
                'message_text': '<a href="{}">{}</a>'.format(url, title),
                'parse_mode': 'HTML'
            }
        }]
        title = 'Twitter Proxy'
        answers.append({
            'type': 'article',
            'id': 2,
            'title': title,
            'input_message_content': {
                'message_text': '\n'.join(CONFIG['TWITTER_PROXY_ADDRESS']),
                'parse_mode': 'HTML'
            }
        })

    else:
        if globalvars.apposlist is None or len(globalvars.apposlist) == 0:
            read_config_file(token)

        answers = []
        docid = 1
        logger.debug('Query {}'.format(query))
        for app, values in globalvars.apposlist.items():
            if query in app.lower():
                url = 'https://telegram.me/PaskoochehBot?start={}'.format(
                    base64.urlsafe_b64encode(app.encode('utf-8')).decode('utf-8'))
                title = app + ' ' + values['version']
                answers.append({
                    'type': 'article',
                    'id': docid,
                    'title': title,
                    'url': url,
                    'hide_url': True,
                    'input_message_content': {
                        'message_text': '<a href="{}">{}</a>'.format(url, title),
                        'parse_mode': 'HTML'
                    }
                })
                docid += 1

    response = {}
    response['inline_query_id'] = inline_query['id']
    response['results'] = json.dumps(
        answers[offset:offset+CONFIG['MAX_INLINE_ANSWERS_COUNT']-1])
    if len(answers) - offset > CONFIG['MAX_INLINE_ANSWERS_COUNT']:
        response['next_offset'] = str(
            offset + CONFIG['MAX_INLINE_ANSWERS_COUNT'] - 1)
    response['cache_time'] = 300
    # response['switch_pm_text'] = globalvars.lang.text('MENU_PM_BOT')  # type: ignore
    # response['switch_pm_parameter'] = query

    telegram.send_inlinequery_answer(token, response)


def get_attachment(bucket, key, name, tool_name, link, lang, text_template_name: str='TEXT_BODY', html_template_name: str='HTML_BODY', attachment_template_name: str='ATTACHMENT_HTML'):
    """ Validate and retrieve attachment file

    Args:
        bucket: s3 bucket where attachment resides
        key: s3 key to attachment
        name: filename to show in email
    Returns:
        text_body: templated text body of email
        html_body: templated html body of email
        file_data: contents of attachment file or None
    """
    attachment_template = TEMPLATES[attachment_template_name][lang]
    text_template = TEMPLATES[text_template_name][lang]
    html_template = TEMPLATES[html_template_name][lang]

    attachment = None
    if bucket and key:
        logger.debug(bucket)
        logger.debug(key)
        attachment = storage.get_object_metadata(bucket, key)

    if not attachment:
        text_body, html_body = feedback.template_email_link(text_template, html_template,
                                                            attachment_template, link)
        file_data = False
    else:
        if attachment.content_length < CONFIG['MAX_ATTACHMENT_SIZE']:
            # attach installer
            try:
                s3_resource = boto3.resource('s3')
                file_data = s3_resource.Object(bucket, key).get()
            except ClientError as error:
                logger.error('Error getting file to attach: %s', str(error))
                raise

            if key[-4:] == '.exe':
                text_template = TEMPLATES['WIN_TEXT_BODY'][lang]
                html_template = TEMPLATES['WIN_HTML_BODY'][lang]

            logger.debug('Sending file: %s', name)
            text_body, html_body = feedback.template_email_link(text_template, html_template,
                                                                attachment_template, None)
        else:
            with open(CONFIG['CONFIDENTIAL_ACCESS']) as conf_sec:
                conf_access = json.load(conf_sec)
                api_key_id = conf_access['LIMITED_ACCESS']['API_KEY_ID']
                secret_key = conf_access['LIMITED_ACCESS']['SECRET_KEY']
            # s3_link = storage.get_temp_link(
            #     bucket, key, CONFIG['API_KEY_ID'], CONFIG['SECRET_KEY'])
            s3_link = storage.get_temp_link(
                bucket, key, api_key_id, secret_key)
            org_link = 'https://{}.s3.amazonaws.com/'.format(
                CONFIG['FILE_S3_BUCKET'])
            mod_link = 'https://s3.amazonaws.com/{}/'.format(
                CONFIG['FILE_S3_BUCKET'])
            s3_link = s3_link.replace(org_link, mod_link)
            logger.debug('File is %s bytes, sending link.',
                        attachment.content_length)
            file_data = False
            text_body, html_body = feedback.template_email_link(text_template, html_template,
                                                                attachment_template, s3_link)
    text_body = text_body.replace('{ tool name }', tool_name)
    html_body = html_body.replace('{ tool name }', tool_name)

    return (text_body, html_body, file_data)


def get_response_from_config(recipient_email, lang):
    """ Get file requested from email destination

    Args:
        recipient_email: email address request was sent to
    Returns:
        matching configuration object from json file
    """
    s3 = boto3.resource('s3')
    s3_file = s3.Object(CONFIG['CONF_S3_BUCKET'],
                        CONFIG['CONF_S3_KEY'])
    stream = s3_file.get()['Body'].read()
    conf_file = json.loads(stream)

    if recipient_email == CONFIG['START_EMAIL']:
        return {
            'html': compose_start_html(conf_file)
        }
    elif recipient_email == CONFIG['REPLY_EMAIL'][lang]:
        return {}
    elif recipient_email == CONFIG['NEWS_EMAIL']:
        return {
            'html': get_news_html()
        }
    elif 'android' in recipient_email and 'paskoocheh-android' not in recipient_email:
        return {
            'apk_issue': ''
        }

    found_tool = None

    for platform in conf_file['versions']:
        for tool in conf_file['versions'][platform]:
            if tool['download_via']['email'] == recipient_email:
                os_name = platform
                found_tool = tool
    if not found_tool:
        raise ValidationError('No matching email address found for request: {}'
                              .format(recipient_email))

    return {
        'bucket': CONFIG['FILE_S3_BUCKET'],
        'key': found_tool['s3_key'][1:],
        'file_name': os.path.basename(found_tool['s3_key']),
        'release_url': found_tool['download_via']['url'],
        'tool_name': found_tool['app_name'] + ' - ' + os_name,
        'tool': found_tool['app_name'],
        'os': os_name,
        'version': found_tool['version_number'],
        'size': found_tool['size'],
        'tool_id': found_tool['tool_id']
    }


def get_news_html():

    try:
        s3_resource = boto3.resource('s3')
        email_body = s3_resource.Object(
            CONFIG['NEWS_BUCKET'], CONFIG['NEWS_FILENAME']).get()['Body'].read()
    except ClientError as error:
        logger.error('Error getting file to attach: %s', str(error))
        raise

    return email_body


def compose_start_html(s3_config):
    """ Compose START_EMAIL html

    Args:
        pb_config: parsed Proto Buffer config file
    Returns:
        HTML to include in the response
    """
    html = u'<html>'
    html += TEMPLATES['BIA_HTML']['style']
    html += TEMPLATES['BIA_HTML']['body_top']

    html += '<tr>'
    html += TEMPLATES['BIA_HTML']['table_header'].format(
        platform_name='Tools')

    Tools = {}
    for platform in s3_config['versions']:
        if not s3_config['versions'][platform] or len(s3_config['versions'][platform]) == 0:
            continue
        html += TEMPLATES['BIA_HTML']['table_header'] \
            .format(platform_name=platform)
        platname = platform
        for tool in s3_config['versions'][platform]:
            if not tool['app_name'] in Tools:
                Tools[tool['app_name']] = {}
            Tools[tool['app_name']][platname] = tool['download_via']['email']
    html += '</tr>'

    for toolname, platforms in Tools.items():
        html += '<tr>'
        html += TEMPLATES['BIA_HTML']['table_first_column'] \
            .format(tool_name=toolname)
        for platform in s3_config['versions']:
            if not s3_config['versions'][platform] or len(s3_config['versions'][platform]) == 0:
                continue
            platname = platform
            if platname in platforms:
                toollink = TEMPLATES['BIA_HTML']['table_tool_link']. \
                    format(tool_maillink=platforms[platname])
            else:
                toollink = ''
            html += TEMPLATES['BIA_HTML']['table_cell'] \
                .format(tool_link=toollink)
        html += '</tr>'

    html += TEMPLATES['BIA_HTML']['body_bottom']
    return html


def parse_ses_notification(ses_notification):
    """ Gather incoming email info and validate

    Args:
        ses_notification: ses object from Lambda event
    Returns:
        source_email, recipient
    """
    if ses_notification['receipt']['spamVerdict']['status'] == 'FAIL':
        raise ValidationError('Email flagged as spam. EMAIL={}'.format(
            ses_notification['mail']['source']))

    if ses_notification['receipt']['virusVerdict']['status'] == 'FAIL':
        raise ValidationError('Email contains virus. EMAIL={}'.format(
            ses_notification['mail']['source']))

    source_email = ses_notification['mail']['source']
    recipient = ses_notification['mail']['destination'][0].lower()
    if 'subject' in ses_notification['mail']['commonHeaders']:
        subject = ses_notification['mail']['commonHeaders']['subject'].lower()
    else:
        subject = ""
    return (source_email, recipient, subject)


def write_to_db(recipient, via, response, lang):
    # store request in Database and send email
    data = {
        'user_uuid': str(recipient),
        'tool': response['tool'],
        'channel': CONFIG['APPLICATION_SOURCE'][lang],
        'platform': response['os'],
        'tool_version': response['version'],
        'platform_version': None,
        'download_time': None,
        'downloaded_via': via,
        'country': None,
        'city': None,
        'network_type': None,
        'file_size': response['size'],
        'network_name': None,
        'channel_version': CONFIG['VERSION'],
        'network_country': None,
        'timezone': None,
        'tool_id': response['tool_id']
    }

    try:
        conn = get_db_connection('STATS_DB')
        database.write_download(data, conn)
        logger.debug('Wrote Download to DB')
    except Exception as exc:
        logger.error(
            'Unable to get_chat_state {}'.format(str(exc)))


def reset_variables():
    globalvars.apposlist = {}
    globalvars.applistos = {}
    globalvars.applistname = {}
    globalvars.categorylist = {}
    globalvars.toolcat = {}
    globalvars.catoslist = {}
    globalvars.namelist = []
    globalvars.oslist = []
    return


def reload_keys_signal(reload_endpoint: str, pool_name: str = 'first_pool') -> bool:
    """Send a reload-keys signal to a Flask app.

    Required values:
      - reload_endpoint (str): API end point of the Flask app
      - pool_name (str): Name of the Outline servers pool

    Optional values with their default values:
    """
    if reload_endpoint is None or len(reload_endpoint)==0:
        logger.error(f'reload_endpoint is missing')
        return False

    post_data = {
        "label": pool_name
    }

    try:
        req = requests.post(f'{reload_endpoint}/reload-keys',
                            data=json.dumps(post_data),
                            verify=False,
                            timeout=3)
    except Exception as err:
        logger.error(
            f'Sending a reload signal to the redis server failed: {err}')
        return False
    if req.status_code != requests.codes['ok']:
        logger.error(
            f'Reload keys request was not successful. status: {req.status_code}')
        return False
    return True


def hash_str(s: str) -> str:
    '''
        Hash a string

        Args:
        s: a string

        Returns:
        hashed string
    '''

    hashed = hashlib.sha512(s.encode('utf-8')).hexdigest()

    return hashed
