""" Email Responder Lambda Function """

from botocore.exceptions import ClientError
from pyskoocheh import feedback
from pyskoocheh.log import Log
from helpers import (
    write_to_db,
    get_promo_code,
    record_exist,
    find_proxy,
    update_ss_config,
    get_attachment,
    get_response_from_config,
    parse_ses_notification,
    reload_keys_signal,
    hash_str)
from settings import CONFIG
from templates import TEMPLATES
from outline_distribution.handler import OutlineHandler
import urllib.parse as url_parse
import time


logger = Log("EmailResponder", is_debug=CONFIG['IS_DEBUG'])


def mail_responder(event, _):
    """ Main entry point to handle the feedback form
        event: information about the email
        context: information about the context
    """
    logger.debug('%s: Request received:%s', __name__,
                str(event['Records'][0]['eventSource']))

    LANG = CONFIG['LANG']

    outline_new_name = "OUTLINE_NEW"
    outline_exist_name = "OUTLINE_EXIST"

    try:
        (source_email, recipient, subject) = parse_ses_notification(
            event['Records'][0]['ses'])
    except Exception as e:
        logger.error("error parsing the SES notification {}".format(e))
        return False

    if 'undisclosed-recipients' in recipient:
        logger.error(
            f"We've got an email to undisclosed-recipients "
            f"Sender: {source_email} "
            f"To: {recipient} "
            f"Subject: {subject}")
        return False

    project = 'paskoocheh'
    lb_type = True
    if subject in CONFIG['OUTLINE_PROJECTS']:
        project = CONFIG['OUTLINE_PROJECTS'][subject]
        lb_type = False

    if '@mada19.org' in recipient:
        LANG = 'ar'
        recipient = recipient.replace('mada19.org', 'paskoocheh.com')

    if '@direme.xyz' in recipient:
        recipient = recipient.replace('direme.xyz', 'paskoocheh.com')

    if '@notofilter.dev' in recipient:
        recipient = recipient.replace('notofilter.dev', 'paskoocheh.com')

    reply_email = CONFIG['REPLY_EMAIL'][LANG]
    email_subject = TEMPLATES['EMAIL_SUBJECT'][LANG]

    if 'icd.community' in recipient:
        LANG = 'en'
        recipient = recipient.replace('icd.community', 'paskoocheh.com')
        project = 'icd'
        reply_email = 'no-reply@icd.community'
        email_subject = TEMPLATES['ICD_EMAIL_SUBJECT'][LANG]
        outline_new_name = "OUTLINE_ICD"
        outline_exist_name = "OUTLINE_ICD"
        lb_type = False

    if 'paskoocheh.com' not in recipient:
        logger.error(
            f"An email to a wrong recipient address "
            f"Sender: {source_email} "
            f"To: {recipient} "
            f"Subject: {subject}")
        return False

    logger.debug("Project is: {}".format(project))

    logger.debug('Source Email {} recipient {}'.format(
        source_email, recipient))

    logger.debug('Start Email: {}'.format(CONFIG['START_EMAIL']))

    if recipient == CONFIG['OUTLINE_EMAIL']:
        if project == 'paskoocheh':
            feedback.send_email(
                reply_email,
                source_email,
                email_subject,
                TEMPLATES['DEPRECATED_TEXT_BODY'][LANG],
                TEMPLATES['DEPRECATED_HTML_BODY'][LANG],
                '',
                None,
                CONFIG['FEEDBACK_EMAIL'])
            return True
        outline = OutlineHandler(None, project, add_prefix=True)
        user_hash = hash_str(source_email)
        try:
            logger.debug(f'source_email: {user_hash}, project: {project}')
            user_exist = outline.get_user(user_hash)
        except Exception as e:
            logger.error("error checking User's profile {}".format(e))
            return False

        if user_exist and user_exist.ss_config and lb_type:
            logger.debug(f'user_exist: {user_exist.__json__}')
            logger.debug(f'ss_config: {user_exist.ss_config}')
            key_name = f"{user_exist.ss_config[0].file_name}.json"
            ss_config_link = "ssconf://s3.amazonaws.com/{}/{}".format(CONFIG['S3_SSCONFIG_BUCKET_NAME'], key_name)
            ss_config_aws_url = (CONFIG['OUTLINE_CONFIG_AWS_URL'] %
                                    url_parse.quote(ss_config_link))
            feedback.send_email(
                reply_email,
                source_email,
                email_subject,
                TEMPLATES[f'{outline_exist_name}_TEXT_BODY'][LANG].
                format(f"{ss_config_aws_url}#{project}"),
                TEMPLATES[f'{outline_exist_name}_HTML_BODY'][LANG].
                format(f"{ss_config_aws_url}#{project}", f"{ss_config_aws_url}#{project}"),
                '',
                None,
                CONFIG['FEEDBACK_EMAIL'])
            return True

        # Legacy distribution system for the sponsored projects
        elif user_exist and not lb_type:
            ss_link, ssconfig_name, ss_prefix = outline.get_sslink(
                user_hash,
                "blocked",
                1)
            if ss_link is None:
                feedback.send_email(
                    reply_email,
                    source_email,
                    email_subject,
                    TEMPLATES['NOSERVER_TEXT_BODY'][LANG],
                    TEMPLATES['NOSERVER_HTML_BODY'][LANG],
                    '',
                    None,
                    CONFIG['FEEDBACK_EMAIL'])
                return True

            try:
                ssconfig_link = update_ss_config(ssconfig_name, ss_link)
                ss_config_aws_url = (CONFIG['OUTLINE_CONFIG_AWS_URL'] %
                        url_parse.quote(ssconfig_link))
            except Exception as e:
                logger.error(f"Unable to prepare ss_config_aws_url: {e}")
                feedback.send_email(
                    reply_email,
                    source_email,
                    email_subject,
                    TEMPLATES['NOSERVER_TEXT_BODY'][LANG],
                    TEMPLATES['NOSERVER_HTML_BODY'][LANG],
                    '',
                    None,
                    CONFIG['FEEDBACK_EMAIL'])
                return False

            feedback.send_email(
                reply_email,
                source_email,
                email_subject,
                TEMPLATES[f'{outline_exist_name}_TEXT_BODY'][LANG].
                format(f"{ss_config_aws_url}#{project}"),
                TEMPLATES[f'{outline_exist_name}_HTML_BODY'][LANG].
                format(f"{ss_config_aws_url}#{project}", f"{ss_config_aws_url}#{project}"),
                '',
                None,
                CONFIG['FEEDBACK_EMAIL'])
            return True

        else:
            logger.debug(f'Creating a user profile for: {user_hash}')
            ss_link, ssconfig_name, ss_prefix = outline.create_user(user_hash)
            if ss_link is None:
                logger.debug(f'No Outline key for: {user_hash}')
                feedback.send_email(
                    reply_email,
                    source_email,
                    email_subject,
                    TEMPLATES['NOSERVER_TEXT_BODY'][LANG],
                    TEMPLATES['NOSERVER_HTML_BODY'][LANG],
                    '',
                    None,
                    CONFIG['FEEDBACK_EMAIL'])
                return True

            try:
                ssconfig_link = update_ss_config(ssconfig_name, ss_link, ss_prefix)
                ss_config_aws_url = (CONFIG['OUTLINE_CONFIG_AWS_URL'] %
                        url_parse.quote(ssconfig_link))
            except Exception as e:
                logger.error(f"Unable to prepare ss_config_aws_url: {e}")
                feedback.send_email(
                    reply_email,
                    source_email,
                    email_subject,
                    TEMPLATES['NOSERVER_TEXT_BODY'][LANG],
                    TEMPLATES['NOSERVER_HTML_BODY'][LANG],
                    '',
                    None,
                    CONFIG['FEEDBACK_EMAIL'])
                return False

            # Wait for Outline servers in the pool to reload their keys
            # ToDo: Find a better way to ensure all servers have reloaded their keys
            time.sleep(3)

            fname = TEMPLATES['OUTLINE_GUIDELINE_PHOTO'][LANG]
            with open(fname, "rb") as image_file:
                feedback.send_email(
                    reply_email,
                    source_email,
                    email_subject,
                    TEMPLATES[f'{outline_new_name}_TEXT_BODY'][LANG].
                    format(f"{ss_config_aws_url}#{project}"),
                    TEMPLATES[f'{outline_new_name}_HTML_BODY'][LANG].
                    format(f"{ss_config_aws_url}#{project}", f"{ss_config_aws_url}#{project}"),
                    fname,
                    image_file.read(),
                    CONFIG['FEEDBACK_EMAIL'])
            return True
        return True

    elif recipient == CONFIG['SOS_EMAIL']:
        with open(CONFIG['SOS_FILE'], "rb") as pdf_file:
            feedback.send_email(
                reply_email,
                source_email,
                email_subject,
                TEMPLATES['SOS_TEXT_BODY'][LANG],
                TEMPLATES['SOS_HTML_BODY'][LANG],
                CONFIG['SOS_FILE'],
                pdf_file.read(),
                CONFIG['FEEDBACK_EMAIL'])
        return True

    elif recipient in ['testme@notofilter.dev', 'testme@paskoocheh.com']:
        logger.debug('Responding to the test email.')
        feedback.send_email(
            reply_email,
            source_email,
            email_subject,
            'a',
            'a',
            '',
            None, CONFIG['FEEDBACK_EMAIL'])
        return True

    elif recipient == CONFIG['TG_PROXY_EMAIL']:
        proxy_tg = find_proxy(source_email, filename=CONFIG['MTPROTO_PROXY_FILE'])

        response = {
            'bucket': None,
            'key': None,
            'file_name': None,
            'release_url': None,
            'tool_name': 'telegram-proxy',
            'tool': 'telegram-proxy',
            'os': None,
            'version': None,
            'size': None,
            'tool_id': None,
        }

        try:
            write_to_db(recipient, 'url', response, LANG)
        except Exception as e:
            logger.error("error writing Telegram Proxy to DB {}".format(e))
            return False

        feedback.send_email(
            reply_email, source_email,
            email_subject,
            TEMPLATES['PROXY_TEXT_BODY'][LANG].format(proxy_tg),
            TEMPLATES['PROXY_HTML_BODY'][LANG].format(proxy_tg, proxy_tg),
            '',
            None,
            CONFIG['FEEDBACK_EMAIL'])
        return True

    # Promo Code
    elif recipient in CONFIG['PROMO_CODE_RECIPIENTS']:
        # response = get_response_from_config(recipient, LANG)

        # response = {
        #     'bucket': None,
        #     'key': None,
        #     'file_name': None,
        #     'release_url': None,
        #     'tool_name': 'mullvad-android',
        #     'tool': 'mullvad-android',
        #     'app': 'gershad',
        #     'os': 'android',
        #     'version': None,
        #     'size': None,
        #     'tool_id': None,
        # }

        values = {
            'user_uuid': str(recipient),
            # 'tool': response['tool'],
            # 'app': response['app'],
            'channel': CONFIG['APPLICATION_SOURCE'][LANG],
            # 'platform': response['os'],
            'tool_version': None,
            'platform_version': None,
            'download_time': None,
            'downloaded_via': 'email',
            'country': None,
            'city': None,
            'network_type': None,
            'file_size': None,
            'network_name': None,
            'channel_version': CONFIG['VERSION'],
            'network_country': None,
            'timezone': None,
            'tool_id': None
        }

        tool_name = recipient.split("@")[0]
        print(tool_name)

        values['tool'] = tool_name
        values['app'] = tool_name.split("-")[0]
        values['platform'] = tool_name.split("-")[1]

        try:
            if record_exist(
                    source_email,
                    values['app'],
                    values['platform'],
                    'EMAIL_RESPONDER',
                    'promocode'):
                logger.debug("User already got the promo code.")
                return True
            else:
                print("User did not get the promo code.")
                code, guide_link = get_promo_code(values, source_email)
                print("after get_promo_code")
                if code:
                    feedback.send_email(
                        reply_email,
                        source_email,
                        email_subject,
                        TEMPLATES['MULLVAD_TEXT_BODY'][LANG].
                        format(
                            code,
                            values['app'],
                            CONFIG["PROMO_CODE_EXPIRY_DATE"],
                            guide_link,
                            guide_link),
                        TEMPLATES['MULLVAD_HTML_BODY'][LANG].
                        format(
                            code,
                            values['app'],
                            CONFIG["PROMO_CODE_EXPIRY_DATE"],
                            guide_link,
                            guide_link),
                        '',
                        '',
                        CONFIG['FEEDBACK_EMAIL'])
            # return True

            #save_chat_state_none(tmsg.user_id, tmsg.chat_id, tmsg.user_info)
        except Exception as e:
            logger.error("error checking for record in db {}".format(e))
            return False

    elif recipient == reply_email:
        logger.info('Response to no-reply ignored')
        return True

    try:
        response = get_response_from_config(recipient, LANG)
    except Exception as e:
        logger.error("error preparing the response {}".format(e))
        return False

    # special case for bia@ address
    if not response:
        # no file available, error
        logger.error('No attachment defined in configuration file')
        return False
    elif 'html' in response:
        feedback.send_email(
            reply_email,
            source_email,
            email_subject,
            TEMPLATES['BIA_TEXT'][LANG],
            response['html'], '',
            None,
            CONFIG['FEEDBACK_EMAIL'])
        return True

    elif 'apk_issue' in response:
        logger.debug('User asked for an android app, responding with Paskoocheh app instead.')
        try:
            response = get_response_from_config("paskoocheh-android@paskoocheh.com", LANG)
            file_bucket = response['bucket']
            file_key = response['key']
            file_name = response['file_name']
            release_url = response['release_url']
            tool_name = response['tool_name']
            text_template_name = 'APK_ISSUE_TEXT_BODY'
            html_template_name = 'APK_ISSUE_HTML_BODY'
            attachment_template_name = 'ATTACHMENT_HTML_PASKOOCHEH'
        except Exception as e:
            logger.error("error getting the attachment {}".format(e))
            return False

    else:
        file_bucket = response['bucket']
        file_key = response['key']
        file_name = response['file_name']
        release_url = response['release_url']
        tool_name = response['tool_name']
        text_template_name = 'TEXT_BODY'
        html_template_name = 'HTML_BODY'
        attachment_template_name = 'ATTACHMENT_HTML'

    try:
        (text_body, html_body, file_data) = get_attachment(
            bucket=file_bucket, key=file_key, name=file_name, tool_name=tool_name, link=release_url, lang=LANG,
            text_template_name=text_template_name, html_template_name=html_template_name, attachment_template_name=attachment_template_name)
    except Exception as e:
        logger.error("error getting the attachment {}".format(e))
        return False

    try:
        write_to_db(recipient, 's3' if file_data else 'url', response, LANG)
    except Exception as e:
        logger.error("error writing to DB {}".format(e))
        return False

    try:
        if file_data:
            feedback.send_email(
                reply_email,
                source_email,
                email_subject,
                text_body,
                html_body,
                file_name,
                file_data['Body'].read(),
                CONFIG['FEEDBACK_EMAIL'])
        else:
            feedback.send_email(
                reply_email,
                source_email,
                email_subject,
                text_body,
                html_body,
                file_name,
                None,
                CONFIG['FEEDBACK_EMAIL'])
    except ClientError as error:
        logger.error('Error sending email: %s', str(error))
        return False

    return True
