#!/bin/bash

# Project config
PROJECT_ROOT=`pwd`
DIST_DIR_NAME="dist"
LAMBDA_CODE_FILE=lambda.zip
LAMBDA_FUNCTION_NAME=${LAMBDA_FUNCTION_NAME}

build() {
  echo "---------------------------"
  echo "Building deployment package"
  echo "---------------------------"
  echo ""

  if [ ! -d deploy ]; then
      mkdir deploy
  fi

  if [ ! -d ${DIST_DIR_NAME} ]; then
      mkdir ${DIST_DIR_NAME}
  fi

  dist_path=${PROJECT_ROOT}/${DIST_DIR_NAME}

  echo "Cleaning up dist and deploy directory ..."
  rm -rf ${dist_path}/*
  rm -rf ${PROJECT_ROOT}/deploy/*

  echo "Copying project files ..."
  cp -rf ${PROJECT_ROOT}/src/* ${dist_path}

  echo "Adding pip libs ..."
  pip3 install -r requirements.txt -t ${dist_path}/
  pip install -U --index-url https://test.pypi.org/simple/ -r test-requirements.txt -t ${dist_path}/
  pip install -U --index-url https://${PYPI_USER}:${PYPI_TOKEN}@${GITLAB_URL}/api/v4/projects/125/packages/pypi/simple --extra-index-url https://pypi.org/simple/ outline-distribution -t ${dist_path}/
  pip install -U --index-url https://${PYSKOOCHEH_PYPI_USER}:${PYSKOOCHEH_PYPI_TOKEN}@${GITLAB_URL}/api/v4/projects/73/packages/pypi/simple --extra-index-url https://pypi.org/simple/ pyskoocheh -t ${dist_path}/

  echo "Adding google directory ..."
  mkdir ${dist_path}/google
  touch ${dist_path}/google/__init__.py

  echo "Adding psycopg2 (Ubuntu version) ..."
  cp -rf ${PROJECT_ROOT}/psy/* ${dist_path}

  echo "Adding pyskoocheh library to the dist directory ..."
  cp -rf ${PROJECT_ROOT}/pyskoocheh/* ${dist_path}

  cd ${dist_path}

  zip -r ${PROJECT_ROOT}/deploy/${LAMBDA_CODE_FILE} *
  cd ${PROJECT_ROOT}
}


build

