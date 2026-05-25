# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.12"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f91f2980-69ea-4d03-a5fa-ece9e09724b8",
# META       "default_lakehouse_name": "lh_Bronze",
# META       "default_lakehouse_workspace_id": "86cfb1d8-84ae-4e97-83d6-6de876acf922",
# META       "known_lakehouses": [
# META         {
# META           "id": "f91f2980-69ea-4d03-a5fa-ece9e09724b8"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ### Antigo script de ingestão

# CELL ********************

import pandas as pd
from tqdm.auto import tqdm
base = "https://synapseaisolutionsa.z13.web.core.windows.net/data/AdventureWorks"

# load list of tables
df_tables = pd.read_csv(f"{base}/adventureworks.csv", names=["table"])

for table in (pbar := tqdm(df_tables['table'].values)):
    pbar.set_description(f"Uploading {table} to lakehouse")

    # download
    df = pd.read_parquet(f"{base}/{table}.parquet")

    # save as lakehouse table
    spark.createDataFrame(df).write.mode('overwrite').saveAsTable(table)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python",
# META   "frozen": true,
# META   "editable": false
# META }

# MARKDOWN ********************

# ### Novo script de ingestão

# CELL ********************

import os
import requests
from tqdm.auto import tqdm

base = "https://synapseaisolutionsa.z13.web.core.windows.net/data/AdventureWorks"

# 1. Baixa a lista de tabelas sem usar Pandas
response = requests.get(f"{base}/adventureworks.csv")
response.raise_for_status()

# Divide as linhas e remove espaços/linhas vazias
tables = [line.strip() for line in response.text.split('\n') if line.strip()]

# 2. Iteração sobre as tabelas
for table in (pbar := tqdm(tables)):
    pbar.set_description(f"Processando {table}")

    # Caminho temporário no sistema de arquivos local do Driver
    local_path = f"/tmp/{table}.parquet"
    url = f"{base}/{table}.parquet"

    # Download via streaming (consome quase zero de memória RAM)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=65536):  # Chunks de 64KB
                f.write(chunk)

    # 3. Spark lê direto do arquivo local (esquema file:///)
    # Isso joga os dados direto para a JVM de forma eficiente
    df = spark.read.parquet(f"file://{local_path}")

    # 4. Salva a tabela no Lakehouse
    df.write.mode('overwrite').saveAsTable(table)

    # 5. Limpa o arquivo temporário para não lotar o disco do Driver
    if os.path.exists(local_path):
        os.remove(local_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
