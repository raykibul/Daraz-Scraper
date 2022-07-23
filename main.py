import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import dzScraper
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


async def main():
    count = 0
    filename = "qna_set.csv"
    file = open(filename, 'a', encoding='UTF-8')
    start_time = time.time()
    categories = dzScraper.parse_categorie_links()
    for cate in categories:
        prodlist = await dzScraper.traverse_a_category(cate)
        for product in prodlist:
            qna_list =  await dzScraper.parse_qna_selenium(product)
            count = count + len(qna_list)
            print(f'Total {count} qna parsed')
            # for qna_item in qna_list:
            #     question = qna_item["question"]
            #     answer = qna_item["answer"]
            #     file.write(f'{question},{answer}\n')
            print("--- %s seconds ---" % (time.time() - start_time))


def parse_qna(driver,counter):
    qna_items = driver.find_elements(By.CLASS_NAME,"qna-list")
    for item in qna_items:
        try:
            question = item.find_elements(By.CLASS_NAME,'qna-content')
            for q in question:
                print(q.get_attribute("innerHTML"))

            counter = counter + len(question)
            print(f'total: {counter} qna parsed')
        except  Exception as e:
            print(f'Exception : {e}')
            raise Exception
    return counter



# def check_qna():
#     counter=0
#     driver = dzScraper.get_driver()
#     wait = WebDriverWait(driver, 10)
#     product_link = "https://www.daraz.com.bd/products/-i208006295-s1158074031.html"
#     driver.get(product_link)
#     next_btn = driver.find_elements(By.CLASS_NAME, "next")[-1]
#     if next_btn is not None:
#         while True:
#             counter= parse_qna(driver, counter)
#             next_btn.click()
#             driver.implicitly_wait(4)
#     return

asyncio.run(main())