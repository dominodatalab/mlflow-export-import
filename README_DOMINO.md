# Domino MLflow Export Import Runbook (Local Testing)

## Prepare environment
1. kubectl forward to mongodb
   ```shell
    kubectl port-forward -n domino-platform svc/mongodb-replicaset 27017:27017
    ```
2. kubectl forward to mlflow container. You need to grab the mlflow pod name in the appropriate namespace.
   For example,
   ```shell
    kubectl port-forward -n domino-platform pod/export-samples-efs-6dbf676894-gkv9w 80:3000
    ```
3. Start an mlflow instance. Go to the root of the project folder and run the following
```shell
./scripts/start_local_mlflow.sh
```

4. Set the following environment variables
   AWS_ACCESS_KEY_ID=
   AWS_SECRET_ACCESS_KEY=
   AWS_DEFAULT_REGION=us-east-1
  
   You need keys which have read-write permissions to the s3 bucket s3://mlflow-export-import-domino-artifacts

-o /Users/sameerwadkar/Documents/GitHub2/domino-mlflow-export-import-internal/export-samples -m http://127.0.0.1:4000 -a s3://mlflow-export-import-domino-artifacts

