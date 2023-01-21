# Notes on DataHub, GCP, and BigQuery

## References

- https://cloud.google.com/iam/docs/creating-custom-roles#iam-custom-roles-create-gcloud
- https://datahubproject.io/docs/metadata-ingestion/source_docs/bigquery

## Commands

```shell
# set project
export PROJECT_ID="<your-project-id>"
gcloud config set project ${PROJECT_ID}
gcloud services enable bigquery.googleapis.com
gcloud services list --project ${PROJECT_ID}

# create role
export ROLE_ID="datahub"
export ROLE_FILE="datahub_service_role.yml"
gcloud iam roles create ${ROLE_ID} --project=${PROJECT_ID} \
  --file=gcloud_setup/${ROLE_FILE}

# create service account
export SERVICE_ACCOUNT_ID=${ROLE_ID}
gcloud iam service-accounts create ${SERVICE_ACCOUNT_ID} \
    --description="DataHub service account" \
    --display-name=${ROLE_ID}

# create binding
export IAM_ROLE_ID="projects/${PROJECT_ID}/roles/datahub"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${ROLE_ID}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="${IAM_ROLE_ID}"

# create and download key
gcloud iam service-accounts keys create key-file \
    --iam-account="${ROLE_ID}@${PROJECT_ID}.iam.gserviceaccount.com"

# provide datahub with credentials to the source
export GOOGLE_APPLICATION_CREDENTIALS=key-file
```

```sql
SELECT * 
FROM `bigquery-public-data.fhir_synthea.patient` 
LIMIT 1000

SELECT * 
FROM `bigquery-public-data.fhir_synthea.patient` 
LIMIT 1000
```
