from datahub.ingestion.run.pipeline import Pipeline
import os

# References
# https://github.com/datahub-project/datahub/blob/master/metadata-ingestion/examples/library/programatic_pipeline.py
# https://github.com/datahub-project/datahub/blob/55357783f330950408e4624b3f1421594c98e3bc/metadata-ingestion/tests/unit/test_pipeline.py

DATAHUB_REST_ENDPOINT = os.environ["DATAHUB_REST_ENDPOINT"]
ATHENA_S3_BUCKET = os.environ["ATHENA_S3_BUCKET"]
AWS_ACCOUNT = os.environ["ACCOUNT_ID"]
AWS_REGION = os.environ["AWS_REGION"]
OWNER = "Data Engineering"
ENVIRONMENT = "DEV"
DATABASE = "sampledb"


def run_pipeline():
    pipeline = Pipeline.create(
        {
            "run_id": "athena-run",
            "source": {
                "type": "athena",
                "config": {
                    "aws_region": AWS_REGION,
                    "work_group": "primary",
                    "s3_staging_dir": f"s3://{ATHENA_S3_BUCKET}/results",
                    "database": DATABASE,
                    "env": ENVIRONMENT,
                },
            },
            "transformers": [
                {
                    "type": "simple_add_dataset_tags",
                    "config": {
                        "tag_urns": [
                            "urn:li:tag:AWS",
                            "urn:li:tag:Amazon Athena",
                            f"urn:li:tag:{AWS_ACCOUNT}",
                            f"urn:li:tag:{AWS_REGION}",
                        ]
                    },
                },
                {
                    "type": "simple_add_dataset_ownership",
                    "config": {
                        "owner_urns": [f"urn:li:corpuser:{OWNER}"],
                        "ownership_type": "DATAOWNER",
                    },
                },
            ],
            "sink": {
                "type": "datahub-rest",
                "config": {"server": DATAHUB_REST_ENDPOINT},
            },
        }
    )

    # Run the pipeline and report the results.
    pipeline.run()
    pipeline.raise_from_status()
    pipeline.pretty_print_summary()


if __name__ == "__main__":
    run_pipeline()
