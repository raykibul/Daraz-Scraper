import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import dzScraper
import time


async def main():
    count = 0
    filename = "qna_set.csv"
    file = open(filename, 'a', encoding='UTF-8')
    start_time = time.time()
    categories = dzScraper.parse_categorie_links()
    for cate in categories:
        prodlist = await dzScraper.traverse_a_category(cate)
        for product in prodlist:
            qna_list = await  dzScraper.parse_qna_product(product)
            count = count + len(qna_list)
            print(f'Total {count} qna parsed')
            for qna_item in qna_list:
                print(qna_item)
                question = qna_item["question"]
                answer = qna_item["answer"]
                file.write(f'{question},{answer}\n')
        print("--- %s seconds ---" % (time.time() - start_time))


asyncio.run(main())
