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



def click_element(driver, xPath):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xPath)))

def main():
    with open("./titleClue.json") as f:
        data = json.load(f)

    driver = webdriver.Chrome()
    driver.set_window_size(1920,1080)
    driver.implicitly_wait(5)

    driver.get("https://worksheetzone.org/crossword-puzzle-maker")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/div'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div'))).click()

    for i in range(10):
        driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div[4]/div[1]').click()
        

    driver.switch_to.alert.accept()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div/div/div/div/div/div'))).click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[3]/div/div/div/div[2]/div/div'))).click()

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id=":r7:"]'))).send_keys('worksheetzone.ad@gmail.com', Keys.ENTER)
    
    time.sleep(5)

    for el in data:
        topic = el["topic"]
        for topic_data in el["data"]:
            title = topic_data["title"]
            list_words =topic_data["words"]

            
            try:
                driver.get("https://worksheetzone.org/crossword-puzzle-maker")

                actions = ActionChains(driver)
                title_element = driver.find_element(By.CSS_SELECTOR,'#content-layer > div > div > div > div:nth-child(2)')
                actions.double_click(title_element).perform()
                actions.send_keys(title).perform()

                # Switch input tab
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[1]/div[3]/div[1]/button[2]'))).click()
                
                input_field = driver.find_element(By.XPATH, '//*[@id="multi-text"]')
                for word in list_words:
                    input_field.send_keys(f'{word["value"]},{word["clue"]}\n')

                layout_tab =WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[2]/div[1]/div[2]/div')))
                layout_tab.click()

                options = driver.find_elements(By.XPATH, '//*[@id=":r5:"]/li')
                option = random.choice(options)
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                option.click()
               
                if random.choice([0,1]):
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[2]/div[2]/div/div[1]/span'))).click()
                
                # Save
                driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div[1]').click()



                title_field = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div[3]/div[1]/div[1]/div[2]/div/div[1]/div[1]/input')
                title_field.send_keys(title)

                des = driver.find_element(By.XPATH, '//*[@id="description-textarea"]')
                des.send_keys('Test')

                language = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div[3]/div[1]/div[2]/div[2]/div/input')
                language.send_keys("English" + Keys.ARROW_DOWN + Keys.ENTER)

                grade = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div/div/div[3]/div[1]/div[2]/div[3]/div/input')
                grade.send_keys(random.choice(["Grade 1", "Grade 2", "Grade 3"]) + Keys.ARROW_DOWN + Keys.ENTER)

                tag = driver.find_element(By.XPATH, "/html/body/div[3]/div[3]/div/div/div/div/div[3]/div[1]/div[2]/div[4]/div/input")
                tag.send_keys(topic + Keys.ENTER)


                topic_data["status"] = "oke"
                with open('./titleClue.json', 'w') as file:
                    json.dump(data, file)
                time.sleep(1000)
            
            except Exception as e:
                print(e)
                topic_data["status"] = "failed"
                with open('./titleClue.json', 'w') as file:
                    json.dump(data, file)
                
            

            



if __name__ == "__main__":
    main()
