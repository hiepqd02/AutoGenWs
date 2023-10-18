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


    for el in data:
        topic = el["topic"]
        for topic_data in el["data"]:
            title = topic_data["title"]
            list_words =topic_data["words"]

            
            try:
                driver.get("https://worksheetzone.org/crossword-puzzle-maker")

                # actions = ActionChains(driver)
                # title_element = driver.find_element(By.CSS_SELECTOR,'#content-layer > div > div > div > div:nth-child(2)')
                # actions.double_click(title_element).perform()
                # actions.send_keys(title).perform()

                # # Switch input tab
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[1]/div[3]/div[1]/button[2]'))).click()
                
                # input_field = driver.find_element(By.XPATH, '//*[@id="multi-text"]')
                # for word in list_words:
                #     input_field.send_keys(f'{word["value"]},{word["clue"]}\n')

                layout_tab =WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[2]/div[1]/div[2]/div')))
                layout_tab.click()
                layout_index = random.choice([1,2,3,4,5])
                # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,f'//*[@id=":r5:"]/li[{layout_index}]'))).click()
                # driver.find_elements(By.XPATH, '//*[@id=":r5:"]/li' )
                options = driver.find_elements(By.XPATH, '//*[@id=":r5:"]/li')
                # option = random.choice(options)
                option = options[-1]
                option.click()

                

                
                # if random.choice([0,1]):
                #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="CROSSWORD"]/div[2]/div/div[2]/div[2]/div/div[1]/span'))).click()
                

                # topic_data["status"] = "oke"
                # with open('./titleClue.json', 'w') as file:
                #     json.dump(data, file)
                time.sleep(1000)
            
            except Exception as e:
                print(e)
                topic_data["status"] = "failed"
                with open('./titleClue.json', 'w') as file:
                    json.dump(data, file)
                
            

            



if __name__ == "__main__":
    main()
