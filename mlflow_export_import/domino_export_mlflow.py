from mlflow_export_import.bulk import export_all
import shutil
import os
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export MLflow")
    parser.add_argument("-o", "--output-folder", required=True)
    parser.add_argument("-m", "--mlflow-tracking-uri", required=True)
    args = parser.parse_args()
    root_path = args.output_folder
    mlflow_tracking_uri =args.mlflow_tracking_ur


    output_folder = os.path.join(root_path, 'export')
    print(output_folder)
    if(os.path.exists(output_folder)):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    os.environ['MLFLOW_TRACKING_URI'] = mlflow_tracking_uri
    print('Starting Exports')
    export_all.export_all(output_folder,export_source_tags=True,notebook_formats=None,use_threads=True)





