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

## Testing if S3 writes work
The project root has a `./export-samples` folder with an export of tiny mlflow instance with artifacts

We need to test that the artifacts from the disk are correctly written to S3

Execute python program `domino_import_mlflow` with the following parameters
```shell
echo ${PWD}
export PYTHONPATH="${PWD}"
python3 mlflow_export_import/domino_import_mlflow.py -o ${PYTHONPATH}/export_samples -m http://127.0.0.1:4000 -a s3://mlflow-export-import-domino-artifacts 
```
You can see all the imported experiments at http://127.0.0.1:4000

And you can see the artifacts have been exported to S3 by visiting the url
http://127.0.0.1:4000/#/experiments/1/runs/2a9ef332f86f48adabcfb49a7a28e301

## Testing Exports
First create a folder to export. Ex
```shell
mkdir ~/mlflow/
```
```shell

echo ${PWD}
export PYTHONPATH="${PWD}"
python3 mlflow_export_import/domino_export_mlflow.py -o ${HOME}/mlflow -m http://127.0.0.1:3000 
```
Once finished go to the folder `~/mlflow/export`. All the experiment/run/model exports are there

## Testing Imports with additional tags from the product solution
Lastly we import the exported data. First restart the local mlflow

```shell
./scripts/start_local_mlflow.sh
```
And then import the mlflow dump

```shell
python3 mlflow_export_import/domino_import_mlflow.py -o ${HOME}/mlflow -m http://127.0.0.1:4000 -a s3://mlflow-export-import-domino-artifacts
```

Go to url - http://127.0.0.1:4000/ to verify that all experiments are imported. So are the models.

In this scenarios the artifacts are not imported. In order to do that, this process has to run inside a pod in the cluster
with the `/artifacts/mlflow` folder mounted.
