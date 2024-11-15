import time
import schedule
from datetime import datetime
import functions
import threading


state_code = 0

def wait_and_fill():
        time.sleep(Instance.time_count(1))
        Instance.fill_the_questions()
        Instance.Submit()

if __name__ == "__main__":
    #url = input('the url: ')
    url = 'https://docs.qq.com/form/page/DUU16elNIR1lubVhu?templateId=fqz3ex8g7tdkdrxra61dd78yac&create_type=2#/fill'
    #url = 'https://docs.qq.com/form/page/DRXZSWlZDT0pWd0hU#/fill'
    #url = 'https://docs.qq.com/form/page/DU3RqT2l3UWluSHVo'

    Instance = functions.Responder(url)
    
    Instance.Login()

    #time.sleep(5)

    start_time = Instance.get_start_time()
    
    list = Instance.fetch_questions()

   # print(Instance.time_count())

    Instance.get_answer()

    wait_thread = threading.Thread(target=wait_and_fill)
    wait_thread.start()