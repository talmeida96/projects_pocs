import fileConvert as etl
import datetime, time

def main():
    start = datetime.datetime.now()

    try:
        etl.convert_to_table()
        time.sleep(0.2)

    except Exception as e:
        print(f'- [EXCEPTION] Main file: {repr(e)}')
        pass
    
    finally:
        print('DONE!')

        print("start: ", start)
        print("end  : ", datetime.datetime.now())
        print("time : ", (datetime.datetime.now() - start))
        
if __name__ == '__main__':
    main()