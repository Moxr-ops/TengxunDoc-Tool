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
    q_count = 0 #问卷上问题的数量
    
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
            select_pos = -1
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
                    select_pos += 1
                    select_choice, lens = self.get_select_text(select_pos, lens)
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
                    'select_pos': select_pos, #select类型问题中的第几个(从0开始)，用于定位表单
                    'user_answer': user_answer
                })
        finally:
            return self.questions
            
    def add_question(self, question_type, locator, answer): #在列表中添加问题，暂时没用
        self.questions.append({
            'type': question_type,
            'locator': locator,
            'answer': answer
        })

    def Drop_Down_Page(self): #下拉问卷网页，暂时没用
        body = self.driver.find_elemen(By.CSS_SELECTOR, 'body')
        actions = ActionChains(self.driver)
        actions.scroll(body)
        actions.perform()

    def fill_text_field(self, data_qid, text): #填充文本类问题
        try:
            selector = f"[data-qid='{data_qid}']"
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            textarea = element.find_element(By.CSS_SELECTOR, "textarea")

            self.driver.execute_script("arguments[0].click();", textarea)
            textarea.send_keys(text)
        finally:
            pass
            #print("try to fill simple...")

    def fill_radio(self, data_qid, options): #填充单选类问题
        try:
            selector = f"[data-qid='{data_qid}'] .form-choice-option.form-choice-radio-option:nth-child({options}) div.form-choice-option-normal.form-choice-radio-option-normal"
            choice = self.driver.find_element(By.CSS_SELECTOR, selector)
            self.driver.execute_script("arguments[0].click();", choice)
        finally:
            time.sleep(0)

    def fill_checkbox(self, data_qid, arr): #填充多选类问题
        try:
            for index in arr:
                selector = f"[data-qid='{data_qid}'] .form-choice.form-choice-checkbox div:nth-child({index}) .form-choice-option-normal.form-choice-checkbox-option-normal"
                choice = self.driver.find_element(By.CSS_SELECTOR, selector)

                self.driver.execute_script("arguments[0].click();", choice)
        finally:
            time.sleep(0)

    def fill_select(self, data_qid, pos, text):
        try:
            #selector = f"[data-qid='{data_qid}'] span.dui-select-arrow.form-select-arrow"
            #dropdown = self.driver.find_element(By.CSS_SELECTOR, selector)
            #if dropdown:
            #    self.driver.execute_script("arguments[0].click();", dropdown)
            #    time.sleep(1)

            #debug_script = """
            #var elements = document.querySelectorAll('.dui-dropdown-content-bottom');
            #if (elements.length > arguments[0]) {
            #    var targetElement = elements[arguments[0]];
            #    var descendants = targetElement.querySelectorAll('.dui-menu-item-text-container');
            #    var texts = [];
            #    descendants.forEach(function(element) {
            #        texts.push(element.textContent.trim());
            #    });
            #    return texts;
            #}
            #return [];
            #"""
            #available_texts = self.driver.execute_script(debug_script, pos)
            #print(f"pos: {pos}, Available options: {available_texts}")
            #print(f"Trying to match: {text}")

            # Script to select the desired option
            script = """
            var elements = document.querySelectorAll('.dui-dropdown-content-bottom');
            if (elements.length > arguments[0]) {
                var targetElement = elements[arguments[0]];
                var descendants = targetElement.querySelectorAll('.dui-menu-item-text-container');
                for (var i = 0; i < descendants.length; i++) {
                    var currentText = descendants[i].textContent.trim();
                    if (currentText === arguments[1]) {
                        return descendants[i];
                    }
                }
                return null;
            }
            return null;
            """
            choice = self.driver.execute_script(script, pos, text)

            if choice:
                #print("Element found, attempting to click")
                self.driver.execute_script("arguments[0].click();", choice)
                time.sleep(0.1)
            else:
                print("未发现匹配元素")

            # Close the dropdown menu
            #if dropdown:
            #    self.driver.execute_script("arguments[0].click();", dropdown)

        except Exception as e:
            print(f"填充select类型问题时发生错误: {str(e)}")
        finally:
            time.sleep(0.5)
    
    def get_answer(self): #获取用户答案
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
                        user_answer = input("请输入选项文本内容: ")
                        #if user_answer.isdigit() and 0 <= int(user_answer) <= 100:
                        #    question['user_answer'] = int(user_answer)
                        #    break
                        if user_answer:
                            question['user_answer'] = user_answer.strip()
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

            print("\n\n\n获取答案完成，等待答题时机...\n")

        except Exception as e:
            print(f"获取答案时发生错误: {str(e)}")
        finally:
            pass
            #print("get answer...")

    def get_select_text(self, pos, lens): #获得下拉表单类问题的选项内容
        try:
            script = f"""
            var parentElements = document.querySelectorAll('.dui-dropdown-content-bottom');
            var secondElement = parentElements[{pos}]; 
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
                content = content + con + "\n"#+ " : " + str(index) + "\n"
            lens = index + 1
            return content, contents

        except Exception as e:
            print(f"获取 select 类型问题的选项文本时发生错误: {str(e)}")
        finally:
            time.sleep(0)

    def fill_the_questions(self): #填充所有问题
        print("\nstart to fill\n")
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
                    if max_attempts < 0:
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
                    if max_attempts < 0:
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
                    if max_attempts < 0:
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
                    if max_attempts < 0:
                        print(f"填写问题“{question['content']}”时失败")
            print("填写完毕")
        except TimeoutException:
            print("在指定时间内元素不可交互")
        finally:
            print("try to fill questions...")
    
    def Submit(self): #提交问卷
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
                time.sleep(0.1)
            finally:
                print("try to submit...")
        if max_attempts < 0:
            print("提交失败")
            sys.exit

    def Login(self): #自动化登录，方便测试和用户使用
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

    def get_start_time(self): #获得问卷开始时间
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
                if max_attempts:
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
                
    def time_count(self, delay): #计算需要等待的时间
        start_time = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M")
        day = start_time.day
        hour = start_time.hour
        minute = start_time.minute
        now = datetime.now()
        start_time0 = now.replace(day= day, hour=hour, minute=minute, second=0, microsecond=0)

        wait_seconds = (start_time0 - now).total_seconds() + delay

        return wait_seconds
    
    def timed_operation(self, func): #到时间自动执行func，由于不太稳定，所以改用上面的函数了
        try:
            run_time = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M")
            schedule.every().day.at(run_time.strftime("%H:%M")).do(func)
            while self.state_code:      
                schedule.run_pending()
                time.sleep(1)
        except Exception as e:
            print(f"失败，原因：{e}")
            sys.exit()

    def test_func(self): #把所有问题的用户答案设置成1，测试用的
        for question in self.questions:
            question['user_answer'] = '1'
        
    def Expand(self): #扩大浏览器页面，暂时没用
        self.driver.set_window_size(5000, 5000)

    def reget_id(self): #测试时发现偶尔会发生获取的id不对应题目的情况，故加此函数，增加代码健壮性
        elements = self.driver.find_elements(By.CSS_SELECTOR, f".{self.questions[0]['data-qid']}")
        if not elements:
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".question")))
                questions = self.driver.find_elements(By.CSS_SELECTOR, ".question")
                for question in questions:  
                    data_qid = question.get_attribute('data-qid')
                    for question in self.questions:
                        question['data-qid'] = data_qid
            except Exception as e:
                print(f"重新获取id时发生错误: {str(e)}")
            finally:
                pass
