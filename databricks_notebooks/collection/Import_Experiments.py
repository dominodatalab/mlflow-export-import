# Databricks notebook source
# MAGIC %md ## Import Experiments
# MAGIC 
# MAGIC Widgets
# MAGIC * Input directory - directory of exported experiments
# MAGIC * Use threads - use multi-threaded import
# MAGIC 
# MAGIC See https://github.com/mlflow/mlflow-export-import/blob/master/README_bulk.md#experiments.

# COMMAND ----------

# MAGIC %sh pip install export-samples-export-import

# COMMAND ----------

dbutils.widgets.text("1. Input directory", "") 
input_dir = dbutils.widgets.get("1. Input directory")
input_dir = input_dir.replace("dbfs:","/dbfs")

dbutils.widgets.dropdown("2. Use threads","no",["yes","no"])
use_threads = dbutils.widgets.get("2. Use threads") == "yes"

print("input_dir:",input_dir)

# COMMAND ----------

if len(input_dir)==0: raise Exception("ERROR: Input directory is required")

# COMMAND ----------

from mlflow_export_import.bulk.import_experiments import import_experiments
import mlflow
import_experiments(
    client=mlflow.tracking.MlflowClient(),
    input_dir=input_dir, 
    use_src_user_id=False, 
    use_threads=use_threads)