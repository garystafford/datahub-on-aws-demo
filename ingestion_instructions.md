# Ingestion Instructions

```shell
DATAHUB_API_POD=""
kubectl cp ingestion $DATAHUB_API_POD:/root -n datahub

kubectl exec -it $DATAHUB_API_POD -n datahub -- bash

cd ~/ingestion/AWS/111222333444/us-east-1/

# install datahub packages
pip install 'acryl-datahub'
pip install 'acryl-datahub[athena]'
pip install 'acryl-datahub[bigquery]'
pip install 'acryl-datahub[s3]'
pip install 'acryl-datahub[dbt]'
pip install 'acryl-datahub[glue]'
pip install 'acryl-datahub[hive]'
pip install 'acryl-datahub[kafka]'
pip install 'acryl-datahub[mongodb]'
pip install 'acryl-datahub[mssql]'
pip install 'acryl-datahub[mysql]'
pip install 'acryl-datahub[postgres]'
pip install 'acryl-datahub[redshift]'
pip install 'acryl-datahub[redshift-usage]'
pip install 'acryl-datahub[snowflake]'
pip install 'acryl-datahub[great-expectations]'
pip install 'acryl-datahub[superset]'

datahub check plugins

# set required environment variables
export DATAHUB_REST_ENDPOINT="http://${DATAHUB_DATAHUB_GMS_PORT_8080_TCP_ADDR}:${DATAHUB_DATAHUB_GMS_PORT_8080_TCP_PORT}"

export ACCOUNT_ID="111222333444" # changes depending on source
export AWS_REGION="us-east-1" # changes depending on source

export ATHENA_S3_BUCKET=""

export AURORA_HOST_PORT=""
export AURORA_USERNAME=""
export AURORA_PASSWORD=""

export MYSQL_HOST_PORT=""
export MYSQL_USERNAME=""
export MYSQL_PASSWORD=""

export MSSQL_HOST_PORT=""
export MSSQL_USERNAME=""
export MSSQL_PASSWORD=""

export POSTGRES_HOST_PORT=""
export POSTGRES_USERNAME=""
export POSTGRES_PASSWORD=""

export REDSHIFT_HOST_PORT=""
export REDSHIFT_USERNAME=""
export REDSHIFT_PASSWORD=""

export REDSHIFT_SERVERLESS_HOST_PORT=""
export REDSHIFT_SERVERLESS_USERNAME=""
export REDSHIFT_SERVERLESS_PASSWORD=""

export KAFKA_BROKERS=""
export KAFKA_SASL_USERNAME=""
export KAFKA_SASL_PASSWORD=""

export DBT_PROJECT_DIRECTORY=""

export MONGODB_CONNECTION_URI=""
export MONGODB_USERNAME=""
export MONGODB_PASSWORD=""

export SNOWFLAKE_HOST_PORT=""
export SNOWFLAKE_USERNAME=""
export SNOWFLAKE_PASSWORD=""
export SNOWFLAKE_ROLE=""

export GOOGLE_APPLICATION_CREDENTIALS=key-file
export GOOGLE_PROJECT_ID=""

env | sort

# optional/informational - get GMS config
curl "http://${DATAHUB_DATAHUB_GMS_SERVICE_HOST}:${DATAHUB_DATAHUB_GMS_SERVICE_PORT}/config"

# ingest aws metadata sources
datahub ingest -c athena_synthea.dhub.yaml
datahub ingest -c athena_tickit.dhub.yaml
datahub ingest -c glue_data_catalog.dhub.yaml
datahub ingest -c msk_kafka.dhub.yaml
datahub ingest -c aurora_postgres_tickit.dhub.yaml
datahub ingest -c rds_mysql_tickit.dhub.yaml
datahub ingest -c rds_mssql_tickit.dhub.yaml
datahub ingest -c rds_postgres_moma.dhub.yaml
datahub ingest -c rds_postgres_pagila.dhub.yaml
datahub ingest -c rds_postgres_tickit.dhub.yaml
datahub ingest -c redshift_provisioned_dev.dhub.yaml
datahub ingest -c redshift_serverless_demo.dhub.yaml
datahub ingest -c redshift_usage_provisioned_dev.dhub.yaml
# permission denied for relation stl_insert < no table in serverless - does not work with serverless
#datahub ingest -c redshift_usage_serverless_demo.dhub.yaml

# ingest non-aws metadata sources
datahub ingest -c google_bigquery.dhub.yaml
datahub ingest -c snowflake.dhub.yamlclear
datahub ingest -c mongodb_atlas.dhub.yaml
datahub ingest -c dbt_redshift_tickit.dhub.yaml

# ingest glossary
datahub ingest -c business_glossary_to_datahub.dhub.yaml
```