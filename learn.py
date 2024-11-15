from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import sys
import time
import functions

#url = 'https://docs.qq.com/form/page/DUU16elNIR1lubVhu?templateId=fqz3ex8g7tdkdrxra61dd78yac&create_type=2#/fill'
#driver.get(url)
url = 'https://docs.qq.com/form/page/DUU16elNIR1lubVhu?templateId=fqz3ex8g7tdkdrxra61dd78yac&create_type=2#/fill'


Instance = functions.Responder(url)

#Instance.Login()
time.sleep(15)

#Instance.Expand()

list = Instance.fetch_questions()

#print(list)
Instance.test_func()

time.sleep(2)
print("ready")

Instance.fill_the_questions()



#for que in list:
#    if que['type'] == 'simple':
#        Instance.fill_text_field(que['data-qid'], 'hello')
#    if que['type'] == 'radio':
#        Instance.fill_radio(que['data-qid'], 2)
#    if que['type'] == 'checkbox':
#        Instance.fill_checkbox(que['data-qid'], 1)
#    lens = 0
#    if que['type'] == 'select':
#        print(que['select_pos'])
#        print(que['user_answer'])
#        Instance.fill_select(que['data-qid'], que['select_pos'], 0)
#Instance.Submit()
#time.sleep(3)
#Instance.Submit()
#Instance.test_func()
#Instance.get_start_time()
#Instance.timed_operation(Instance.fill_the_questions)
