import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import paho.mqtt.client as mqtt
import os
import json

load_dotenv()

broker_addr = os.getenv('MQTT_URL')
broker_port = int(os.getenv('MQTT_PORT'))
broker_topic =  os.getenv('MQTT_AGRO_TOPIC')
broker_user = os.getenv('MQTT_AGRO_USERNAME')
broker_pw = os.getenv('MQTT_AGRO_PASSWORD')

payload_lst = []
json_data = []
payload_data = None
client = None

def connect_mqtt():
    global client
    global broker_addr
    global broker_pw
    global broker_user
    global broker_port

    if client is None:
        print("- [BROKER] Creating new instance")
        client = mqtt.Client("python-agro-broker")
        client.username_pw_set(broker_user, broker_pw)
        client.on_connect = on_connect
        client.on_message = on_message

        print("- [BROKER] Connecting to broker: ", broker_addr)
        client.connect(broker_addr, broker_port)

    return client

def on_connect(client, userdata, flags, rc):
    global broker_topic

    if rc == 0:
        print(f"- [BROKER] Connection OK. Subscribing to topic: {broker_topic}")
        client.subscribe(broker_topic)
    else:
        print("- [BROKER] Bad connection: returned code= ", rc)

def on_message(client, userdata, message):
    global payload_lst
    global payload_data
    
    try:
        payload_data = json.loads( message.payload )
        payload_data["received_at"] = datetime.now()
        
        payload_lst.append( payload_data )
        
        convert_to_table()

    except Exception as e:
        print(f'- [EXCEPTION] on_message_function: {repr(e)}')
        # pass

def convert_to_table():
  global payload_lst
  global json_data

  # Criação de DataFrame vazio
  df = pd.DataFrame()
  
  # Extração dos dados do Payload
  for payload_data in payload_lst:
    for sensor in payload_data["sensors"]:
      sensor_code = sensor["code"]
      sensor_mod_id = sensor["mod_id"]
      sensor_data = sensor["data"]
      
      # Criação de DataFrame temporário para cada variação de sensores
      temp_df = pd.DataFrame(sensor_data)
      
      temp_df["deviceid"] = payload_data["deviceid"]
      temp_df["fw_ver"] = payload_data["fw_ver"]

      temp_df["timestamp"] = pd.to_datetime(payload_data['timestamp'], unit='s', utc=True)
      temp_df["sensor_code"] = sensor_code
      temp_df["sensor_mod_id"] = sensor_mod_id

      # Concatenação dos 2 DataFrames
      df = pd.concat([df, temp_df])
    
    # Ordenação das colunas
    df = df[["deviceid", "fw_ver", "timestamp", "sensor_code", "sensor_mod_id", "id_unit", "value"]]
    
    # Reseta o index do DataFrame
    df.reset_index(drop=True, inplace=True)
    
    print("-----------------------------------------------------------------------")
    print(df)