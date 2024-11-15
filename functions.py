from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import schedule
from datetime import datetime, timedelta

import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class Responder:
    q_count = 0
    
    def __init__(self, url):
        edge_driver_path = 'D:/github/tengxunwendang/msedgedriver.exe'
        service = Service(executable_path=edge_driver_path)

        options = webdriver.EdgeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--ignore-certificate-errors')
       # options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)
        driver = webdriver.Edge(service=service, options=options)

        self.driver = driver
        self.questions = []
        self.url = url

        self.driver.get(self.url)

    def fetch_questions(self):

        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".question")))
            questions = self.driver.find_elements(By.CSS_SELECTOR, ".question")
            self.q_count = len(self.driver.find_elements(By.CSS_SELECTOR, ".question"))
            select_sum = 0
            print(f"\n共有{self.q_count}个问题")

            for question in questions:  
                type = question.get_attribute('data-type')
                content = question.find_element(By.CSS_SELECTOR, "div.question-title .form-auto-ellipsis").text
                data_qid = question.get_attribute('data-qid')
                lens = 0
                
                if type == 'radio':
                    radio_choice = question.find_element(By.CSS_SELECTOR, ".form-choice.form-choice-radio").text
                else:
                    radio_choice = None
                if type == 'checkbox':
                    checkbox_choice = question.find_element(By.CSS_SELECTOR, ".form-choice.form-choice-checkbox").text
                else:
                    checkbox_choice = None
                if type == 'select':
                    select_sum += 1
                    select_choice = self.get_select_text(select_sum, lens)
                else:
                    select_choice = None 
                user_answer = None
                self.questions.append({
                    'type': type,
                    'data-qid': data_qid,
                    'content': content,
                    'radio_choice': radio_choice,
                    'checkbox_choice': checkbox_choice,
                    'select_choice': select_choice, #下拉表单中的内容
                    'select_len': lens, #下拉表单中选项个数
                    'select_pos': select_sum, #select类型问题中的第几个，用于定位表单
                    'user_answer': user_answer
                })
        finally:
            return self.questions
            
    def add_question(self, question_type, locator, answer):
        self.questions.append({
            'type': question_type,
            'locator': locator,
            'answer': answer
        })

    def Drop_Down_Page(self):
        body = self.driver.find_elemen(By.CSS_SELECTOR, 'body')
        actions = ActionChains(self.driver)
        actions.scroll(body)
        actions.perform()

    def fill_text_field(self, data_qid, text):
        try:
            selector = f"[data-qid='{data_qid}']"
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            textarea = element.find_element(By.CSS_SELECTOR, "textarea")

            self.driver.execute_script("arguments[0].click();", textarea)
            textarea.send_keys(text)
        finally:
            print("try to fill simple...")

    def fill_radio(self, data_qid, options):
        try:
            selector = f"[data-qid='{data_qid}'] .form-choice-option.form-choice-radio-option:nth-child({options}) div.form-choice-option-normal.form-choice-radio-option-normal"
            choice = self.driver.find_element(By.CSS_SELECTOR, selector)
            self.driver.execute_script("arguments[0].click();", choice)
        finally:
            time.sleep(0)

    def fill_checkbox(self, data_qid, arr):
        try:
            for index in arr:
                selector = f"[data-qid='{data_qid}'] .form-choice.form-choice-checkbox div:nth-child({index}) .form-choice-option-normal.form-choice-checkbox-option-normal"
                choice = self.driver.find_element(By.CSS_SELECTOR, selector)

                self.driver.execute_script("arguments[0].click();", choice)
        finally:
            time.sleep(0)

    def fill_select(self, data_qid, pos, index):
        try:
            selector = f"[data-qid='{data_qid}'] span.dui-select-arrow.form-select-arrow"
            dropdown = self.driver.find_element(By.CSS_SELECTOR, selector)
            if dropdown:
                self.driver.execute_script("arguments[0].click();", dropdown)
                time.sleep(0.3)

            script = """
            var elements = document.querySelectorAll('.dui-dropdown-content-inner');
            if (elements.length > arguments[0]) { 
                var targetElement = elements[arguments[0]];
                var descendants = targetElement.querySelectorAll('.dui-menu-item-text-container'); 
                if (descendants.length > arguments[1]) { 
                    var descendant = descendants[arguments[1]]; 
                    return descendant;
                } else {
                    return null;
                }
            } else {
                return null;
            }
            elements.forEach(function(element) {
                texts.push(element.textContent);
            });
            """
            choice = self.driver.execute_script(script, pos, index)
            if choice:
                self.driver.execute_script("arguments[0].click();", choice)

            selector = f"[data-qid='{data_qid}'] span.dui-select-arrow.form-select-arrow"
            dropdown = self.driver.find_element(By.CSS_SELECTOR, selector)
            if dropdown:
                self.driver.execute_script("arguments[0].click();", dropdown)

        finally:
            time.sleep(0)
    
    def get_answer(self):
        try:
            for question in self.questions:
                while True:
                    print(f"\n问题: {question['content']}")

                    if question['type'] == 'radio':
                        print(f"选项: \n{question['radio_choice']}")
                        user_answer = input("请输入选项序号: ")
                        if user_answer.isdigit() and 1 <= int(user_answer) <= 4:
                            question['user_answer'] = int(user_answer)
                            break

                    elif question['type'] == 'checkbox':
                        print(f"选项: {question['checkbox_choice']}")
                        answer = input("请输入选项序号(多个用逗号分隔): ")
                        try:
                            user_answer = [int(item.strip()) for item in answer.split(',')]
                            if all(1 <= x <= 4 for x in user_answer):
                                question['user_answer'] = user_answer
                                break
                            else:
                                print("请输入有效的选项序号（1-4）")
                        except ValueError:
                            print("输入格式错误，请使用逗号分隔的数字")

                    elif question['type'] == 'select':
                        print(f"选项: {question['select_choice']}")
                        user_answer = input("请输入选项序号: ")
                        if user_answer.isdigit() and 0 <= int(user_answer) <= 100:
                            question['user_answer'] = int(user_answer)
                            break

                    elif question['type'] == 'simple':
                        user_answer = input("请输入回答: ").strip()
                        if user_answer:
                            question['user_answer'] = user_answer
                            break

                    else:
                        print(f"未知的问题类型: {question['type']}")
                        break

                    print("输入无效，请重新输入")

            print("获取答案完成，等待答题时机...")

        except Exception as e:
            print(f"获取答案时发生错误: {str(e)}")
        finally:
            print("get answer...")

    def get_select_text(self, index, lens):
        try:
            script = f"""
            var parentElements = document.querySelectorAll('.dui-dropdown-content-bottom');
            var secondElement = parentElements[{index-1}]; 
            var elements = secondElement.querySelectorAll('.dui-menu-item-text-container');
            var texts = [];
            elements.forEach(function(element) {{
                texts.push(element.textContent);
            }});
            return texts;
            """
            contents = self.driver.execute_script(script)

            content = ''
            index = -1
            for con in contents:
                index += 1
                content = content + con + " : " + str(index) + "\n"
            lens = index + 1
            return content

        except Exception as e:
            print(f"获取 select 类型问题的选项文本时发生错误: {str(e)}")
        finally:
            time.sleep(0)

    def fill_the_questions(self):
        print("start fill")
        try:
            for question in self.questions:
                if question['type'] == 'simple':
                    max_attempts = 10
                    while max_attempts >= 0:
                        try:
                            self.fill_text_field(question['data-qid'], question['user_answer'])
                            print(f"成功填写问题：“{question['content']}”")
                            break
                        except Exception as e:
                            print(f"填充simple时发生错误: {str(e)}")
                            max_attempts -= 1
                            time.sleep(0.1)
                    print(f"填写问题“{question['content']}”时失败")
                if question['type'] == 'radio':
                    max_attempts = 10
                    while max_attempts >= 0:
                        try:
                            self.fill_radio(question['data-qid'], question['user_answer'])
                            print(f"成功填写问题：“{question['content']}”")
                            break
                        except Exception as e:
                            print(f"填充radio时发生错误: {str(e)}")
                            max_attempts -= 1
                            time.sleep(0.1)
                    print(f"填写问题“{question['content']}”时失败")
                if question['type'] == 'checkbox':
                    max_attempts = 10
                    while max_attempts >= 0:
                        try:
                            self.fill_checkbox(question['data-qid'], question['user_answer'])
                            print(f"成功填写问题：“{question['content']}”")
                            break
                        except Exception as e:
                            print(f"填充checkbox时发生错误: {str(e)}")
                            max_attempts -= 1
                            time.sleep(0.1)
                    print(f"填写问题“{question['content']}”时失败")
                if question['type'] == 'select':
                    max_attempts = 10
                    while max_attempts >= 0:
                        try:
                            self.fill_select(question['data-qid'], question['select_pos'], question['user_answer'])
                            print(f"成功填写问题：“{question['content']}”")
                            break
                        except Exception as e:
                            print(f"填充select时发生错误: {str(e)}")
                            max_attempts -= 1
                            time.sleep(0.1)
                    print(f"填写问题“{question['content']}”时失败")
            print("填写完毕")
        except TimeoutException:
            print("在指定时间内元素不可交互")
        finally:
            print("try to fill questions...")
    
    def Submit(self):
        max_attempts = 10
        while max_attempts >= 0:
            try:
                submit = self.driver.find_element(By.CSS_SELECTOR, '.question-commit button')
                self.driver.execute_script("arguments[0].click();", submit)
                submit = self.driver.find_element(By.CSS_SELECTOR, '.dui-button.dui-modal-footer-ok.dui-button-type-primary.dui-button-size-default')
                self.driver.execute_script("arguments[0].click();", submit)
                break
            except Exception as e:
                print(f"提交时发生错误: {str(e)}")
                max_attempts -= 1
                time.sleep(0.2)
            finally:
                print("try to submit...")
        print("提交失败")
        sys.exit

    def Login(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#header-login-btn')))
            submit = self.driver.find_element(By.CSS_SELECTOR, '#header-login-btn')
            self.driver.execute_script("arguments[0].click();", submit)

            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.dui-checkbox.dui-checkbox-normal.dui-checkbox-tick input[type="checkbox"]')))
            submit = self.driver.find_element(By.CSS_SELECTOR, '.dui-checkbox.dui-checkbox-normal.dui-checkbox-tick input[type="checkbox"]')
            self.driver.execute_script("arguments[0].click();", submit)

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#layout > div.dui-tabs.top-tab-bar-pc > div.dui-tabs-bar-container > ul > li:nth-child(1)')))
            submit = self.driver.find_element(By.CSS_SELECTOR, '#layout > div.dui-tabs.top-tab-bar-pc > div.dui-tabs-bar-container > ul > li:nth-child(1)')
            self.driver.execute_script("arguments[0].click();", submit)

        except Exception as e:
            pass
        finally:
            print("Login...")

    def get_start_time(self):
        max_attempts = 3
        while max_attempts >= 0:
            try:
                raw_time_element = self.driver.find_element(By.CSS_SELECTOR, ".form-header-time-setting")
                raw_time = raw_time_element.find_element(By.CSS_SELECTOR, "div.form-header-setting-group.form-header-setting-child > div > div:nth-child(2)").text
                break
            except Exception as e:
                print(f"获取时间时发生错误: {str(e)}")
                max_attempts -= 1

                max_attempts = 5
                while max_attempts >= 0:
                    try:
                        self.start_time = input("请手动输入时间（格式：%Y-%m-%d %H:%M）：")
                        start_time = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M")
                        current_time = datetime.now()
                        if start_time > current_time:
                            print(f"获取时间成功，自动填写程序将在{self.start_time}启动")
                            return self.start_time
                        else:
                            print("开始时间不是在未来，程序启动失败")
                            sys.exit()
                    except ValueError:
                         print("输入的时间格式不正确，请重新输入。")
                         max_attempts -= 1
                print("获取时间失败，程序结束")
                sys.exit()
        try:
            raw_time = raw_time.split("开始")[0]
            current_year = datetime.now().year
            start_time_str = f"{current_year}-{raw_time}"
            self.start_time = start_time_str
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M") 
            current_time = datetime.now()
            if start_time > current_time:
                print(f"获取时间成功，自动填写程序将在{self.start_time}启动")
                self.state_code = 1
                return self.start_time
            else:
                print("开始时间不是在未来，程序启动失败")
                sys.exit()
        finally:
            pass
                
    def time_count(self, delay):
        start_time = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M")
        day = start_time.day
        hour = start_time.hour
        minute = start_time.minute
        now = datetime.now()
        start_time0 = now.replace(day= day, hour=hour, minute=minute, second=0, microsecond=0)

        wait_seconds = (start_time0 - now).total_seconds() + delay

        return wait_seconds
    
    def timed_operation(self, func):
        try:
            run_time = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M")
            schedule.every().day.at(run_time.strftime("%H:%M")).do(func)
            while self.state_code:      
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            print(f"失败，原因：{e}")
            sys.exit()

    def test_func(self):
        for question in self.questions:
            question['user_answer'] = '1'
        
    def Expand(self):
        self.driver.set_window_size(5000, 5000)