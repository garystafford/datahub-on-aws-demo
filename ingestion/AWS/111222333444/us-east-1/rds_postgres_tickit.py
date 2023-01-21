# Purpose: Programmatic DataHub pipline example
# Author: Gary A. Stafford
# Created: 2022-03-15
# Updated: 2023-01-16

import json
import logging

import boto3
from botocore.exceptions import ClientError
from datahub.ingestion.run.pipeline import Pipeline

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    sts_client = boto3.client("sts")

    params = get_parameters()
    params["owner"] = "Database Administrators"
    params["environment"] = "DEV"
    params["database"] = "tickit"
    params["region"] = sts_client.meta.region_name
    params["account"] = sts_client.get_caller_identity()["Account"]
    logging.info(f"Params: {json.dumps(params, indent=4, sort_keys=True)}")

    ingestion_pipeline = create_pipeline(params)
    run_pipeline(ingestion_pipeline)


def create_pipeline(params) -> Pipeline:
    """Constructs a Pipeline for a PostgreSQL Source and a DataHub Sink

    :return: instance of datahub.ingestion.run.pipeline
    """

    pipeline = Pipeline.create(
        {
            "run_id": "postgres-run",
            "source": {
                "type": "postgres",
                "config": {
                    "host_port": params.get("/datahub_demo/postgres_host_port_tickit"),
                    "database": params.get("database"),
                    "username": params.get("/datahub_demo/postgres_username_tickit"),
                    "password": params.get("/datahub_demo/postgres_password_tickit"),
                    "profiling": {"enabled": "true"},
                    "env": params.get("environment"),
                },
            },
            "transformers": [
                {
                    "type": "simple_add_dataset_tags",
                    "config": {
                        "tag_urns": [
                            f"urn:li:tag:AWS",
                            f"urn:li:tag:Amazon RDS for PostgreSQL",
                            f"urn:li:tag:{params.get('account')}",
                            f"urn:li:tag:{params.get('region')}",
                        ]
                    },
                },
                {
                    "type": "pattern_add_dataset_terms",
                    "config": {
                        "term_pattern": {
                            "rules": {
                                ".*users.*": [
                                    "urn:li:glossaryTerm:Classification.Sensitive"
                                ]
                            }
                        }
                    },
                },
                {
                    "type": "simple_add_dataset_ownership",
                    "config": {
                        "owner_urns": [f"urn:li:corpuser:{params.get('owner')}"],
                        "ownership_type": "DATAOWNER",
                    },
                },
            ],
            "sink": {
                "type": "datahub-rest",
                "config": {
                    "server": params.get("/datahub_demo/datahub_rest_endpoint_private")
                },
            },
        }
    )

    return pipeline


def run_pipeline(pipeline):
    """Runs the ingestion pipeline and prints summary of the results

    :param pipeline: instance of datahub.ingestion.run.pipeline
    :return:
    """

    pipeline.run()
    pipeline.pretty_print_summary()


def get_parameters() -> dict:
    """
    Load parameter values from AWS Systems Manager (SSM) Parameter Store

    :return: dict of parameter k/v's
    """

    ssm_client = boto3.client("ssm")
    params: dict = {}

    try:
        # make a single SSM API call for all parameters
        response = ssm_client.get_parameters_by_path(Path="/datahub_demo")

        # create a dictionary of parameter k/v's
        for param in response.get("Parameters"):
            params[param["Name"]] = param["Value"]

        logging.debug(f"Params: {params}")
    except ClientError as e:
        logging.error(e)
        exit(1)

    return params


if __name__ == "__main__":
    main()
