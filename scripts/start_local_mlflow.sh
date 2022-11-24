#!/bin/bash
rm ${PWD}/root/mlflow/*
mkdir -p ${PWD}/root/mlflow/
MLFLOW_TRACKING_URI="sqlite:///${PWD}/root/mlflow/mlflow.db"
MLFLOW_UI_URI="http://127.0.0.1:4000"
mlflow server -p 4000 --backend-store-uri ${MLFLOW_TRACKING_URI} --default-artifact-root s3://export-samples-export-import-domino-artifacts --host 0.0.0.0