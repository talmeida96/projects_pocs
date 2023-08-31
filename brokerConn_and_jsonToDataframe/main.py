import brokerConnection as broker
import time

def main():
    client = broker.connect_mqtt()
    client.loop_start()
    
    try:
        while True:
            time.sleep(0.2)

    except Exception as e:
        print(f'- [EXCEPTION] Main file: {repr(e)}')
        pass
    
    finally:
        client.loop_stop()
        print('- [INFO] Client disconnected')
        
if __name__ == '__main__':
    main()