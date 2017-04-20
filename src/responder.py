""" Email Responder Lambda Function """

import logging
import os
import boto3
from botocore.exceptions import ClientError
from pyskoocheh import actionlog, storage, feedback
from pyskoocheh.errors import ValidationError
import protobuf.schemas.python.paskoocheh_pb2 as paskoocheh
from settings import CONFIG

LANG = CONFIG["LANG"]
LOGGER = logging.getLogger()
LOGGER.setLevel(CONFIG["LOG_LEVEL"])

def parse_ses_notification(ses_notification):
    """ Gather incoming email info and validate

    Args:
        ses_notification: ses object from Lambda event
    Returns:
        source_email, recipient
    """
    if ses_notification["receipt"]["spamVerdict"]["status"] == "FAIL":
        raise ValidationError("Email flagged as spam.")

    if ses_notification["receipt"]["virusVerdict"]["status"] == "FAIL":
        raise ValidationError("Email contains virus.")

    source_email = ses_notification["mail"]["source"]
    recipient = ses_notification["mail"]["destination"][0].lower()
    return (source_email, recipient)

def compose_start_html(pb_config):
    """ Compose START_EMAIL html

    Args:
        pb_config: parsed Proto Buffer config file
    Returns:
        HTML to include in the response
    """
    html = u"<html>"
    html += CONFIG["TEMPLATES"]["BIA_HTML"]["style"]
    html += CONFIG["TEMPLATES"]["BIA_HTML"]["body_top"]

    html += "<tr>"
    html += CONFIG["TEMPLATES"]["BIA_HTML"]["table_header"].format(platform_name = "Tools")

    Tools = {}
    for platform in pb_config.platforms:
        if not platform.tools or len(platform.tools) == 0:
            continue
        html += CONFIG["TEMPLATES"]["BIA_HTML"]["table_header"] \
            .format(platform_name = paskoocheh.PlatformName.Name(platform.name).title())
        platname = paskoocheh.PlatformName.Name(platform.name).title()
        for tool in platform.tools:
            if not tool.contact.name in Tools:
                Tools[tool.contact.name] = {}
            Tools[tool.contact.name][platname] = tool.contact.mail_responder_email
    html += "</tr>"

    for toolname, platforms in Tools.items():
        html += "<tr>"
        html += CONFIG["TEMPLATES"]["BIA_HTML"]["table_first_column"] \
                .format(tool_name = toolname)
        for platform in pb_config.platforms:
            if not platform.tools or len(platform.tools) == 0:
                continue
            platname = paskoocheh.PlatformName.Name(platform.name).title()
            if platname in platforms:
                toollink = CONFIG["TEMPLATES"]["BIA_HTML"]["table_tool_link"]. \
                           format(tool_maillink = platforms[platname])
            else:
                toollink = ""
            html += CONFIG["TEMPLATES"]["BIA_HTML"]["table_cell"] \
                     .format(tool_link = toollink)
        html += "</tr>"

    html += CONFIG["TEMPLATES"]["BIA_HTML"]["body_bottom"]
    return html

def get_news_html():

    try:
        s3_resource = boto3.resource("s3")
        email_body = s3_resource.Object(CONFIG["NEWS_BUCKET"], CONFIG["NEWS_FILENAME"]).get()['Body'].read()
    except ClientError as error:
        LOGGER.error("Error getting file to attach: %s", str(error))

    return email_body

def get_requested_file_config(recipient_email):
    """ Get file requested from email destination

    Args:
        recipient_email: email address request was sent to
    Returns:
        matching configuration object from json file
    """
    pb_file = storage.get_binary_contents(CONFIG["CONF_S3_BUCKET"], CONFIG["CONF_S3_KEY"])
    pb_config = paskoocheh.Config()
    pb_config.ParseFromString(pb_file["Body"].read())

    if recipient_email == CONFIG["START_EMAIL"]:
        return {
            "html": compose_start_html(pb_config)
        }
    elif recipient_email == CONFIG["REPLY_EMAIL"]:
        return {}
    elif recipient_email == CONFIG["NEWS_EMAIL"]:
        return {
            "html": get_news_html()
        }

    found_tool = None
    for platform in pb_config.platforms:
        for tool in platform.tools:
            if tool.contact.mail_responder_email == recipient_email:
                os_name = paskoocheh.PlatformName.Name(platform.name).title()
                found_tool = tool
    if not found_tool:
        raise ValidationError("No matching email address found for request: {}"
                              .format(recipient_email))

    return {
        "bucket": CONFIG["CONF_S3_BUCKET"],
        "key": found_tool.releases[0].binary.path,
        "file_name": os.path.basename(found_tool.releases[0].binary.path),
        "release_url": found_tool.releases[0].release_url,
        "tool_name": found_tool.contact.name + " - " + os_name
    }

def get_attachment(bucket, key, name, tool_name, link):
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
    attachment_template = CONFIG["TEMPLATES"]["ATTACHMENT_HTML"][LANG]
    text_template = CONFIG["TEMPLATES"]["TEXT_BODY"][LANG]
    html_template = CONFIG["TEMPLATES"]["HTML_BODY"][LANG]

    attachment = None
    if bucket and key:
        attachment = storage.get_object_metadata(bucket, key[1:])

    if not attachment:
        text_body, html_body = feedback.template_email_link(text_template, html_template,
                                                            attachment_template, link)
        file_data = False
    else:
        if attachment.content_length < CONFIG["MAX_ATTACHMENT_SIZE"]:
            # attach installer
            try:
                s3_resource = boto3.resource("s3")
                file_data = s3_resource.Object(bucket, key[1:]).get()
            except ClientError as error:
                LOGGER.error("Error getting file to attach: %s", str(error))

            if key[-4:] == ".exe":
                text_template = CONFIG["TEMPLATES"]["WIN_TEXT_BODY"][LANG]
                html_template = CONFIG["TEMPLATES"]["WIN_HTML_BODY"][LANG]

            LOGGER.info("Sending file: %s", name)
            text_body, html_body = feedback.template_email_link(text_template, html_template,
                                                                attachment_template, None)
        else:
            s3_link = storage.get_temp_link(bucket, key[1:],
                                         CONFIG["API_KEY_ID"], CONFIG["SECRET_KEY"])
            s3_link = s3_link.replace("https://paskoocheh.s3.amazonaws.com/", "https://s3.amazonaws.com/paskoocheh/")
            LOGGER.info("File is %s bytes, sending link.", attachment.content_length)
            file_data = False
            text_body, html_body = feedback.template_email_link(text_template, html_template,
                                                                attachment_template, s3_link)
    text_body = text_body.replace("{ tool name }", tool_name)
    html_body = html_body.replace("{ tool name }", tool_name)

    return (text_body, html_body, file_data)

def mail_responder(event, _):
    """ Main entry point to handle the feedback form
        event: information about the email
        context: information about the context
    """
    LOGGER.info("%s: Request received:%s", __name__, str(event["Records"][0]["eventSource"]))

    (source_email, recipient) = parse_ses_notification(event["Records"][0]["ses"])

    if recipient != CONFIG["START_EMAIL"] and recipient != CONFIG["NEWS_EMAIL"]:
        if actionlog.is_limit_exceeded(source_email, recipient.split("@")[0]):
            LOGGER.error("Rate limit exceeded for email:%s requested file:%s, Exiting",
                         source_email, recipient.split("@")[0])
            return False

    response = get_response_from_config(recipient)

    # special case for bia@ address
    if not response:
        # no file available, error
        LOGGER.error("No attachment defined in configuration file")
        return False
    else:
        file_bucket = response["bucket"]
        file_key = response["key"]
        file_name = response["file_name"]
        release_url = response["release_url"]
        tool_name = response["tool_name"]

    (text_body, html_body, file_data) = get_attachment(file_bucket, file_key, file_name, tool_name, release_url)

    # store request in dynamodb and send email
    actionlog.log_action(source_email, recipient.split("@")[0], CONFIG["SOURCE_APP"])
    try:
        if file_data:
            feedback.send_email(CONFIG["REPLY_EMAIL"], source_email,
                                CONFIG["EMAIL_SUBJECT"], text_body, html_body, file_name,
                                file_data["Body"].read(),
                                CONFIG["FEEDBACK_EMAIL"])
        else:
            feedback.send_email(CONFIG["REPLY_EMAIL"], source_email,
                                CONFIG["EMAIL_SUBJECT"], text_body, html_body, file_name,
                                None,
                                CONFIG["FEEDBACK_EMAIL"])
    except ClientError as error:
        LOGGER.error("Error sending email: %s", str(error))

    return True
