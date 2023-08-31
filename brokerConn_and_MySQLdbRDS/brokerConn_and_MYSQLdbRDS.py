import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import os

load_dotenv()

broker_address = os.getenv('MQTT_BROKER')
port = int(os.getenv('MQTT_PORT'))
topic = os.getenv('MQTT_DATA_TOPIC')
broker_user = os.getenv('MQTT_USERNAME')
broker_pw = os.getenv('MQTT_PASSWORD')

# CREDENCIAIS RDS MYSQL [AWS]
config = {
    'user': 'user',
    'password': 'password',
    'host': 'mydb.123456789012.us-east-1.rds.amazonaws.com',
    'database': 'database',
    'raise_on_warnings': True
}

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("- [BROKER] Connected OK")
            print("- [BROKER] Subscribing to topic", topic)
            client.subscribe(topic)

        else:
            print("- [BROKER] Bad connection: returned code= ", rc)

    print("- [BROKER] Creating new instance")
    client = mqtt.Client("brokerScript")
    client.username_pw_set("username", "password")
    client.on_connect = on_connect

    print("- [BROKER] Connecting to broker: ", broker_address)
    client.connect(broker_address, 1883)

    return client

def subscribe(client):
    def on_message(client, userdata, message):
        print(
            "_____________________________________________________________________________________________________________________________________________")
        print("- [MESSAGE] received: ", message.payload)
        print(
            "_____________________________________________________________________________________________________________________________________________")
        print("- [MESSAGE] topic=", message.topic)
        print("- [MESSAGE] qos=", message.qos)
        print("- [MESSAGE] retain flag=", message.retain)

        try:
            json_pkg = message.payload.decode('utf-8')

            if len(json_pkg) > 20:

                db_connection = mysql.connector.connect(**config)
                print("- [MYSQL] Connected successfully!")

                cursor = db_connection.cursor()

                add_json = ("INSERT INTO database.jsonAgro (payload) VALUES (%s)")
                # Insert new json file
                cursor.execute(add_json, [json_pkg])

                # Make sure data is committed to the database
                db_connection.commit()

                cursor.close()
                db_connection.close()

            else:
                print("- [MESSAGE] bad format payload")

        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print("- [MYSQL] Database doesn't exist!")
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("- [MYSQL] Username or password is incorrect!")
            else:
                print(error)

    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()