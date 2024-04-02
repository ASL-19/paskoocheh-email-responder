#!/bin/bash

# Project config
PROJECT_ROOT=`pwd`
DIST_DIR_NAME="dist"
DEPLOY_DIR_NAME="deploy"
LAMBDA_CODE_FILE=lambda.zip
 

# AWS Config
REGION=${REGION}
LAMBDA_HANDLER=${LAMBDA_HANDLER}
##########################
# Fill in before deploying
#PROJECT=paskoochehResponder_prod
LAMBDA_FUNCTION_NAME=${LAMBDA_FUNCTION_NAME}
AWS_ACCOUNT=${AWS_ACCOUNT}
LAMBDA_ROLE=${LAMBDA_ROLE}
LAMBDA_DESCRIPTION="Paskoocheh Email Responder"
##########################
LAMBDA_TIMEOUT=${LAMBDA_TIMEOUT}
LAMBDA_MEMORY=${LAMBDA_MEMORY}
## Python version
RUNTIME=python3.8
## TAGS
TAG_ACCOUNT=${TAG_ACCOUNT}
TAG_PROJECT=${TAG_PROJECT}
TAG_PURPOSE=${TAG_PURPOSE}


update_env_variables() {
  # update function
  echo "----------------------------"
  echo "Update Environment Variables"
  echo "----------------------------"
  echo "Lambda role:"
  echo ${LAMBDA_ROLE}
  AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
  aws lambda update-function-configuration \
    --region ${REGION} \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --handler ${LAMBDA_HANDLER} \
    --description "${LAMBDA_DESCRIPTION}" \
    --role arn:aws:iam::${AWS_ACCOUNT}:role/${LAMBDA_ROLE} \
    --runtime ${RUNTIME} \
    --timeout ${LAMBDA_TIMEOUT} \
    --memory-size ${LAMBDA_MEMORY} \
    --environment '{"Variables": {"DEBUG": "False"}}'
}



update_lambda() {
  # update function
  echo "-----------------------------"
  echo "Update Lambda function on AWS"
  echo "-----------------------------"
  echo ""
  AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
  aws lambda update-function-code \
    --region ${REGION} \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --zip-file fileb://${DEPLOY_DIR_NAME}/${LAMBDA_CODE_FILE}
}

publish_lambda() {
  # update function
  echo "-----------------------------"
  echo "Publish Lambda function on AWS"
  echo "-----------------------------"
  echo ""
  AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}  
  VERSION=(`aws lambda publish-version \
    --region ${REGION} \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --query 'Version' | sed 's/\"//g'`)
  echo ${VERSION}

 aws lambda update-alias \
   --region ${REGION} \
   --function-name ${LAMBDA_FUNCTION_NAME} \
   --name stable \
   --function-version ${VERSION}
}

create_lambda() {
  # create new function
  echo "-----------------------------"
  echo "Create Lambda function on AWS"
  echo "-----------------------------"
  echo ""
  AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
  aws lambda create-function \
    --region ${REGION} \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --description "${LAMBDA_DESCRIPTION}" \
    --zip-file fileb://${DEPLOY_DIR_NAME}/${LAMBDA_CODE_FILE}  \
    --role arn:aws:iam::${AWS_ACCOUNT}:role/${LAMBDA_ROLE} \
    --handler ${LAMBDA_HANDLER} \
    --runtime ${RUNTIME} \
    --timeout ${LAMBDA_TIMEOUT} \
    --memory-size ${LAMBDA_MEMORY} \
    --tags Account=${TAG_ACCOUNT},Project=${TAG_PROJECT},Purpose=${TAG_PURPOSE}
}

clean() {
  echo "---------------------"
  echo "Clean project folders"
  echo "---------------------"
  echo ""
  AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}  
  rm -r ${PROJECT_ROOT}/deploy &> /dev/null
  rm -r ${PROJECT_ROOT}/${DIST_DIR_NAME} &> /dev/null
}


deploy() {
  echo "-----------------------"
  echo "Deploying to AWS Lambda"
  echo "-----------------------"
  echo ""

  # if function already exists
  if aws lambda get-function --region ${REGION} --function-name ${LAMBDA_FUNCTION_NAME} > /dev/null; then
    update_lambda
    sleep 30
    update_env_variables
    sleep 30
    publish_lambda
  else
    create_lambda
    sleep 30
    update_env_variables
  fi
}


deploy
#if [ "$CLEAN" = true ]; then
#    clean
#fi

#if [ "$DEPLOY" = true ]; then
#    deploy
#fi

