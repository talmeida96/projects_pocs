import pandas as pd
from dateutil.parser import isoparse
import json

# FOR JSON FILES
file_path = "/file_path/file_name.json"

with open(file_path, 'r') as json_file:
    data_frame = json.load(json_file)

def convert_to_table():
  global json_data
  # Criação de DataFrame vazio
  df = pd.DataFrame()

  # Extração dos dados do Payload
  for payload_data in data_frame:
    for sensor in payload_data["sensors"]:
      sensor_code = sensor["code"]
      sensor_mod_id = sensor["mod_id"]
      sensor_data = sensor["data"]
      
      # Criação de DataFrame temporário para cada variação de sensores
      temp_df = pd.DataFrame(sensor_data)
      
      temp_df["deviceid"] = payload_data["deviceid"]
      temp_df["fw_ver"] = payload_data["fw_ver"]

      # Converte a data ISO 8601 para timestamp (int64)
      timestamp_iso = payload_data["timestamp"]['$date']
      timestamp = int(isoparse(timestamp_iso).timestamp())

      temp_df["timestamp"] = pd.to_datetime(timestamp, unit='s', utc=True)

      temp_df["sensor_code"] = sensor_code
      temp_df["sensor_mod_id"] = sensor_mod_id
       
      # Concatenação dos 2 DataFrames
      df = pd.concat([df, temp_df])
    
  # Ordenação das colunas
  df = df[["deviceid", "fw_ver", "timestamp", "sensor_code", "sensor_mod_id", "id_unit", "value"]]
  
  # Reseta o index do DataFrame
  df.reset_index(drop=True, inplace=True)
  
  print(df)

  df.to_csv('file_name.csv')