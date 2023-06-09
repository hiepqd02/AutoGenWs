from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import time
import json
from selenium.webdriver.chrome.options import Options


URL = "https://staging.worksheetzone.org/word-search-maker"

# Selector 
WORK_SEARCH_TITLE = "#mui-1"
WORK_SEARCH_CREATOR = "#mui-2"


STUDENT_NAME = "#mui-3"
STUDENT_GRADE = "#mui-4"

WORD_LIST = "#multi-text"

DROP_DOWN_ICON = ".drop-down-icon"
SHAPE_OPTIONS = "div.drop-down > div"
CHECK_BOX_SIZE = ".checkbox-size"

SHOW_ANSWER_CHECKBOX = "#left-word-search-id > div > div.end-check-box > div:nth-child(1) > span > input"
DIRECTION_CHECKBOX = "#left-word-search-id > div > div.end-check-box > div:nth-child(2) > span > input"
SHOW_WORD_LIST = "#left-word-search-id > div > div.end-check-box > div:nth-child(3) > span > input"

MENU_DIRECTIONS = "#left-word-search-id > div > div.word-directions > div:nth-child(2) "
WORD_DIRECTION_OPTIONS = "#menu- > div> ul>li"


WORD_LIST = "#multi-text"
BUTTON_NAME = "#left-word-search-id > div > div.student-info > div.input-info > div:nth-child(1) > div > div > button"
BUTTON_GRADE = "#left-word-search-id > div > div.student-info > div.input-info > div:nth-child(2) > div > div > button"

SAVE_BUTTON = "div.right-header > button"
LOADING = ".new-loading-component"
CONFIRM_BUTTON = "div.confirm"


def init_browser():
    chrome_driver = webdriver.Chrome()
    chrome_driver.set_window_size(1920, 1080)
    chrome_driver.get(URL)
    return chrome_driver

def open_test_page(driver):
    time.sleep(2)
    title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#left-word-search-id > div > div.simple-input > div:nth-child(1) > div.title")))
    for _ in range(10):
        title.click()


def fill_input(driver, locator, input):
    element = driver.find_element(By.CSS_SELECTOR, locator)
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(input)

def set_category_id(driver, categoryId):
    element = driver.find_element(By.CSS_SELECTOR, WORD_LIST)
    driver.execute_script(f"arguments[0].setAttribute('categoryId', {categoryId});", element)



def set_student_info(driver):
    name_btn = driver.find_element(By.CSS_SELECTOR, BUTTON_NAME)
    grade_btn = driver.find_element(By.CSS_SELECTOR, BUTTON_GRADE)
    flag = random.randint(1, 3)

    if flag == 1:
        grade_btn.click()
    elif flag == 2:
        name_btn.click()
        name_btn.click()
    

def fill_list_word(driver, keywords):
    word_list_box = driver.find_element(By.CSS_SELECTOR, WORD_LIST)
    i = 0 
    for keyword in keywords:
        keyword = keyword.replace(".", "")
        try:
            word_list_box.send_keys(keyword.strip())  
            time.sleep(0.1)
            word_list_box.send_keys(Keys.ENTER)
        except ElementNotInteractableException:
            confirm_button = driver.find_element(By.CSS_SELECTOR, CONFIRM_BUTTON)
            driver.execute_script("arguments[0].click();", confirm_button)
            word_list_box.send_keys(Keys.ENTER)
            if i == 5:
                break
            else:
                i += 1


def select_random_shape(driver):
    driver.find_element(By.CSS_SELECTOR, DROP_DOWN_ICON).click()
    time.sleep(1)
    options = driver.find_elements(By.CSS_SELECTOR,SHAPE_OPTIONS)
    option = random.choice(options)
    option.click()

def select_random_size(driver):
    options = driver.find_elements(By.CSS_SELECTOR, CHECK_BOX_SIZE)
    option = random.choice(options)
    option.click()
        
def select_random_directions(driver):
    driver.find_element(By.CSS_SELECTOR, MENU_DIRECTIONS).click()
    time.sleep(1)
    options = driver.find_elements(By.CSS_SELECTOR,WORD_DIRECTION_OPTIONS)
    option = random.choice(options)
    option.click()


def random_show_word_list(driver):
    if random.choice([True, False]):
        show_direction_box = driver.find_element(By.CSS_SELECTOR, DIRECTION_CHECKBOX)
        show_direction_box.click()


def save_ws(driver):
    try:
        save_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, SAVE_BUTTON)))
        save_button.click()
    except Exception as e:
        print(e)
        time.sleep(10000)
def new_browser(chrome_driver,categoryId, title, keywords):
    chrome_driver.get(URL)
    time.sleep(1)
    open_test_page(chrome_driver)
    time.sleep(1)
    fill_input(chrome_driver, WORK_SEARCH_TITLE, title)
    set_student_info(chrome_driver)

    select_random_shape(chrome_driver)
    
    select_random_size(chrome_driver) 

    select_random_directions(chrome_driver)

    random_show_word_list(chrome_driver)

    fill_list_word(chrome_driver, keywords)

    set_category_id(chrome_driver,categoryId)

    save_ws(chrome_driver)

    try:
        WebDriverWait(chrome_driver, 10).until(EC.invisibility_of_element((By.CSS_SELECTOR, LOADING)))
        time.sleep(1)
        chrome_driver.quit()
    except TimeoutError:
        print("Can't save")
    

def main():

        with open("keywordWordSearch.json") as file:
            data = json.load(file)
        topic_index = 0
        ws_created = 0

        for topic in data:
            print(f"Topic index: {topic_index+1}")
            print(f"Ws Created: {ws_created}")
            
            topic_index +=1
            
            topic["parentIds"].append(topic["categoryId"])
            categoryId = topic["parentIds"]

            for ws in topic["data"]:
                title = ws["title"]
                topic_keywords = sorted(ws["words"], key=len, reverse=True)

                options = Options()
                options.add_argument('--headless')
                chrome_driver = webdriver.Chrome()
                chrome_driver.set_window_size(1920, 1080)
                time.sleep(1)
                try:
                    new_browser(chrome_driver, categoryId, title, topic_keywords)
                    ws_created += 1
                
                except Exception as e:
                    print(e)




if __name__ == "__main__":
    main()



