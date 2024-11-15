from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
from datetime import datetime
import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

edge_driver_path = 'D:/github/tengxunwendang/msedgedriver.exe'
service = Service(executable_path=edge_driver_path)

options = webdriver.EdgeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('lang=zh_CN.UTF-8')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("detach", True)

driver = webdriver.Edge(service=service, options=options)

url = 'https://docs.qq.com/form/page/DUU16elNIR1lubVhu?templateId=fqz3ex8g7tdkdrxra61dd78yac&create_type=2#/fill'
driver.get(url)

time.sleep(1)

elements = driver.find_elements(By.CSS_SELECTOR, ".question")
#print(elements)
for element in elements:
#    id = element.get_attribute('placeholder')
#    text = element.find_element(By.CSS_SELECTOR, "div.question-title").text
#    index = element.find_elements(By.CSS_SELECTOR, "i.inumber")
#    a = element.get_attribute('data-type') == 'radio'
     data_qid = element.get_attribute('data-qid')
#    
#
#    radio_choice = element.find_element(By.CSS_SELECTOR, ".question-content.readonly").text
#selector = f"[data-qid='{data_qid}']"
#b = driver.find_element(By.CSS_SELECTOR, selector)
#btxt = b.find_element(By.CSS_SELECTOR, ".form-ui-component-basic-text")
#btxt.clic()
#try:
#    driver.get(url)
#    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".question")))
#    questions = driver.find_elements(By.CSS_SELECTOR, ".question")
#    q_count = len(driver.find_elements(By.CSS_SELECTOR, ".question"))
#    question_list = []
#
#    for question in questions:  
#        type = question.get_attribute('data-type')
#        content = question.find_element(By.CSS_SELECTOR, "div.question-title .form-auto-ellipsis").text
#            
#        question_info = (type, content)
#        question_list.append(question_info)
#finally:
#    time.sleep(0)
#
#print(question_list, q_count)
#index = driver.find_element(By.CSS_SELECTOR, "span.icon-number i.inumber").text
#print(index)

#driver.quit()

#selector = f".dui-dropdown-content-bottom:nth-of-type(1) .dui-menu-item-text-container"#/*[contains(@class, 'dui-menu-item-text-container')][1]"#:nth-of-type(1)"# .dui-menu.dui-menu-normal.dui-select-list"
#contents = driver.find_element(By.XPATH, "(//*[contains(@class, 'dui-dropdown-content-bottom')])[2]//*[contains(@class, 'dui-menu-item-text-container')][3]/text()")
#print(contents)
#for content in contents:
#     print(content.text)
#var elements = document.querySelectorAll('.dui-menu-item-text-container');
#elements.forEach(function(element) {
#  console.log(element.textContent);
#});
a = 1  # 如果您想要获取第二个元素，索引应该是1

# 执行 JavaScript 代码
# 这里使用 f-string 来插入 Python 变量 a 的值
#script = f"""
#var parentElements = document.querySelectorAll('.dui-dropdown-content-bottom');
#var secondElement = parentElements[{a}];  // 使用 a 的值作为索引
#var elements = secondElement.querySelectorAll('.dui-menu-item-text-container');
#var texts = [];
#elements.forEach(function(element) {{
#    texts.push(element.textContent);
#}});
#return texts;
#"""
#
## 使用 execute_script 方法执行 JavaScript 代码，并获取返回的文本列表
#text_list = driver.execute_script(script)
#
## 打印获取到的文本内容列表
#for text in text_list:
#    print(text)

#option_selector = f"div.dui-dropdown-content-inner:nth-child(2) .dui-menu-item-text-container"
#option = driver.find_element(By.CSS_SELECTOR, option_selector)
#option = option.get_attribute('data-dui-1-9-1')
#print(option)
#pos = 1
#index = 1
#script0 = """
#var elements = document.getElementsByClassName('.dui-dropdown-content-inner');
#if (elements.length > arguments[0]) { 
#    var targetElement = elements[arguments[0]];
#    var descendants = targetElement.querySelectorAll('.dui-select-list-container'); 
#    if (descendants.length > arguments[1]) { 
#        var descendant = descendants[arguments[1]]; 
#        return descendant;
#    } else {
#        return null;
#    }
#} else {
#    return null;
#}
#elements.forEach(function(element) {
#    texts.push(element.textContent);
#});
#"""
#
#script1 = """
#var elements = document.querySelectorAll('.dui-dropdown-content-inner');
#var targetElement = elements[4];
#return targetElement;
#"""
#
#script = """
#var elements = document.querySelectorAll('.dui-dropdown-content-inner');
#if (elements.length > arguments[0]) { 
#    var targetElement = elements[arguments[0]];
#    var descendants = targetElement.querySelectorAll('.dui-menu-item-container'); 
#    if (descendants.length > arguments[1]) { 
#        var descendant = descendants[arguments[1]]; 
#        return descendant;
#    } else {
#        return null;
#    }
#} else {
#    return null;
#}
#elements.forEach(function(element) {
#    texts.push(element.textContent);
#});
#"""
#choice = driver.execute_script(script, 0, 2)
#
#print(choice)
#
#result = driver.execute_script(script1)
#
#print (result)
#
#if result and hasattr(result, 'tagName'):  # 如果result是一个元素
#    print("找到了元素:", result.tagName)
#else:
#    print("没有找到元素，或者返回的是文本数组")

#script = """
#// 定位下拉菜单的容器
#var selectContainer = document.querySelector('.dui-select-container');
#
#// 检查下拉菜单是否存在
#if (selectContainer) {
#  // 触发下拉菜单的点击事件以展开选项
#  selectContainer.click();
#
#  // 等待下拉菜单展开
#  setTimeout(function() {
#    // 定位所有选项
#    var options = document.querySelectorAll('.dui-dropdown-container .dui-menu-item');
#
#    // 遍历选项，找到匹配的文本并点击
#    for (var i = 0; i < options.length; i++) {
#      if (options[i].textContent.trim() === '{option_text}') {
#        options[i].click();
#        break;
#      }
#    }
#  }, 500);  // 等待500毫秒，确保下拉菜单已经展开
#}
#"""
#
## 将选项文本传递给JavaScript代码
#script = script.format(option_text='是')
#
## 执行JavaScript代码
#driver.execute_script(script)
#
time.sleep(10)
raw_time = driver.find_element(By.CSS_SELECTOR, ".form-header-time-setting")
print(raw_time)
raw_time = raw_time.find_element(By.CSS_SELECTOR, "div.form-header-setting-group.form-header-setting-child > div > div:nth-child(2)").text
raw_time = raw_time.split("开始")[0]
current_year = datetime.now().year
time = f"{current_year}-{raw_time}"
print(time)