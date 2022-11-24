from mlflow_export_import.experiment.import_experiment import ExperimentImporter
from mlflow_export_import.bulk import import_models,import_experiments
import mlflow
import os

import boto3
import argparse



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Export MLflow")
    parser.add_argument("-o", "--export-folder-root", required=True)
    parser.add_argument("-m", "--mlflow-tracking-uri", required=True)
    parser.add_argument("-a", "--dest-artifact-location", required=True)
    args = parser.parse_args()
    print(os.environ['AWS_SECRET_ACCESS_KEY'])
    client = boto3.client('s3')

    experiment_export_folder = os.path.join(args.export_folder_root, 'export')
    models_export_folder = os.path.join(experiment_export_folder, 'models')
    os.environ['MLFLOW_TRACKING_URI'] = args.mlflow_tracking_uri
    dest_artifact_location = args.dest_artifact_location
    client = mlflow.tracking.MlflowClient()
    print(dest_artifact_location)
    import_models.import_all(client, experiment_export_folder, delete_model=False, use_src_user_id=True,
                             artifact_location=dest_artifact_location,
                             verbose=True, use_threads=False)

