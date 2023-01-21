# Purpose: Container to run DataHub CLI from
# Author: Gary A. Stafford
# Created: 2022-05-17
# Updated: 2023-01-08
# ERROR: Failed building wheel for sasl3: https://stackoverflow.com/questions/48562383/sasl-saslwrapper-h2223-fatal-error-sasl-sasl-h-no-such-file-or-directory

FROM python:3.10.9

# install useful utilities
RUN apt update \
    && apt update -y \
    && apt install git jq curl wget tar bash vim telnet dnsutils libsasl2-dev -y

# install datahub cli/api
RUN pip install --upgrade pip wheel setuptools \
    && pip cache purge \
    && pip install --upgrade acryl-datahub \
    && datahub version

# install datahub source/sink plugins
RUN pip install \
    'acryl-datahub[athena, bigquery, dbt, glue, hive, kafka, mongodb,  \
    mssql, mysql, postgres, redshift, redshift-usage, s3, snowflake, great-expectations, superset]' \
    && datahub check plugins
