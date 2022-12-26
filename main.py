import time
import os
import json
from selenium import webdriver
from multiprocessing import Pool

# options
options = webdriver.ChromeOptions()
# add folder to download files
options.add_experimental_option("prefs", {"download.default_directory": "C:\\Users\\python\\TLA\\openAI_struktura_selenium_serpstat_mt\\chromedriver\\result", "safebrowsing.enabled":"false"})
# headless mode (without open window)
# options.add_argument("--headless")
# silent mode, disable console output
options.add_argument("--log-level=3")


def serpstat_worker(file_name_from_list):
    try:
        # get data from file with the structure
        name_of_file = open(f'result/{file_name_from_list}')
        data = json.load(name_of_file)
        article_title = data['headline'][0].replace('"','')
        list_of_questions = data['structure']+data['faq']

        # launch webdriver
        driver = webdriver.Chrome(
            executable_path="C:\\Users\\TLA\\openAI_struktura_selenium_serpstat_mt\\chromedriver\\chromedriver.exe",
            options=options
        )
        # https://selenium-python.readthedocs.io/waits.html
        driver.implicitly_wait(120) # seconds

        # Step #1: get login
        print("Start > Step #1: get login")
        driver.get("https://testlab.serpstat.com/Article_builder")
        api_key_input = driver.find_element("xpath", '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div/div[1]/div/div[6]/ul/li/div[2]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/div/input')
        api_key_input.send_keys("XXXXXXXXXXXXXXXXXXXXXXXXXXXX") # Serpstat API Key
        button_set_token = driver.find_element("xpath", '//button[text()="💡 Set token"]')
        button_set_token.click()

        time.sleep(5)

        # Step #2: set title for article
        print("Start > Step #2: set title for article")
        set_the_title = driver.find_element("xpath", '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div/div[1]/div/div[11]/div[1]/div/div[1]/div/div[1]/div/input')
        set_the_title.send_keys(article_title)
        button_set_title = driver.find_element("xpath", '//button[text()="✅ Set title and use my outline"]')
        button_set_title.click()

        time.sleep(5)

        # Step #3: set the article structure
        print("Start > Step #3: set the article structure")
        article_outline_textarea = driver.find_element("xpath", '//*[@id="root"]/div[1]/div[1]/div/div/div/section[2]/div/div[1]/div/div[12]/div[1]/div/div[1]/div/div[1]/div/textarea')
        for question in list_of_questions:
            question = question+'\n'
            article_outline_textarea.send_keys(question)
        button_generate_text = driver.find_element("xpath", '//button[text()="📝 Generate text for all paragraphs"]')
        button_generate_text.click()

        # Step #4: get some coffe, relax and whait Serpstat
        print("Start > Step #4: get some coffe, relax and whait Serpstat")
        driver.implicitly_wait(1000) # set new time
        download_button = driver.find_element("xpath", '//button[text()="Download (.html)"]')
        download_button.click()
        print('Done >>>  ' + article_title)
        time.sleep(5)
        with open('log.txt', 'a') as log_file:
            article_title = article_title+'\n'
            log_file.write(article_title)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def multip():
    p = Pool(processes=3) # count of threeds
    list_of_files = os.listdir('C:\\Users\\python\\TLA\\openAI_struktura_selenium_serpstat_mt\chromedriver\\files-with-article-structure')
    for i in range(0, len(list_of_files)):
        p.apply_async(serpstat_worker, args={list_of_files[i]})
        print('Poll == '+str(i))
    
    p.close()
    p.join()

if __name__ == '__main__':
    multip()


    # p = Pool(processes=3)
    # list_of_files = os.listdir('C:\\Users\\TLA\\openAI_struktura_selenium_serpstat_mt\chromedriver\\files-with-article-structure')
    # p.map(serpstat_worker, list_of_files)