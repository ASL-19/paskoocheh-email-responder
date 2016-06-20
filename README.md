# Email Responder File Service
## Requirements

* Python 2.7
* pip

## Setup & Configuration
### File System

* Make a copy of the repository and fill in the configuration details there. This avoids potentially overwriting a running lambda with incorrect config

### S3 Bucket with Downloads

* File structure should be as follows:

        s3://<bucket>
            /conf.json
            /<application name>
                /<OS name>
                    /<file name>

* Create an IAM user with list/download permissions on the target S3 bucket. These credentials go in the settings.py file
* Make sure your `LAMBDA_ROLE` has access to the s3 bucket, as only the temporary links are generated with the credentials in settings.py
* configuration file should have the following structure
  * For each download to be served:

        [{
            "name": "<downloadName>",
            "os": "<downloadOSName>",
            "filename": "<downloadFileName>",
            "email_addr": "<autoresponderEmail>",
            "body": [[
                "plain", "<emailPlainBody>"
            ], [
                "html", "<emailHTMLBody>"
            ]],
            "attachments": [[
                "<downloadBucket>",
                "<downloadBucketKey>",
                "<emailFilename>"
            ]]
        }]

* `downloadBucketKey` should have a leading /, this is trimmed by the email responder bot
* point settings.py at configuration file in JSON in bucket with `S3_BUCKET_NAME` and `S3_CONF_BUCKET_KEY`

### SES

* Set up a forwarding rule that sends applicable email addresses to the email responder lambda using 'Event' invocation
* Make sure you have verified all the domains you want to send emails from

### Python
#### Configuration options in settings.py

Setting | Description
------- | -----------
SOURCE_APP | Name of application (for dynamodb source)
API_KEY_ID | AWS API Key Id for temporary S3 access
SECRET_KEY | AWS Secret Key for temporary S3 access
CONF_S3_BUCKET | Bucket that holds configuration and downloads
CONF_S3_KEY | S3 key of the configuration json
REPLY_EMAIL | Reply email for responses
EMAIL_SUBJECT | Reply subject for responses

### Lambda
#### Deployment settings in install.sh

Setting | Description
------- | -----------
REGION | AWS region to deploy in
PROJECT | Name of Lambda in AWS
AWS_USERID | ID of main AWS account
LAMBDA_ROLE | IAM role with permissions to DynamoDB, SES and S3
LAMBDA_DESCRIPTION | Description of service
LAMBDA_TIMEOUT | AWS Lambda timeout
LAMBDA_MEMORY | AWS Lambda memory limit

## Installation

* Run install.sh to install dependencies and create/update lambda

**note**: if Lambda function already exists, the code will be updated, but will not set any of the configuration options.  If you wish to reset the deployment settings, delete the lambda and re-create.

### For Linux

Some distros have very old versions of pip, if you get errors during installation, uninstall your system pip version and use the method described [here](https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py)
