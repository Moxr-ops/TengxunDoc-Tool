import time
import schedule
from datetime import datetime
import functions
import threading

import style


state_code = 0

def wait_and_fill():
    Instance.reget_id()
    time.sleep(Instance.time_count(0))
    Instance.fill_the_questions()
    Instance.Submit()

if __name__ == "__main__":
    #url = input('the url: ')
    #url = 'https://docs.qq.com/form/page/DUU16elNIR1lubVhu?templateId=fqz3ex8g7tdkdrxra61dd78yac&create_type=2#/fill'
    #url = 'https://docs.qq.com/form/page/DRXZSWlZDT0pWd0hU#/fill'
    #url = 'https://docs.qq.com/form/page/DRVVVdVd4eWpVZFR5#/edit'

    style.show_welcome()

    url = input("\n请输入腾讯文档地址：\n")

    Instance = functions.Responder(url)
    
    Instance.Login()

    start_time = Instance.get_start_time()
    
    list = Instance.fetch_questions()

    Instance.get_answer()

    wait_thread = threading.Thread(target=wait_and_fill)
    wait_thread.start()