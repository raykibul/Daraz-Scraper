import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup
import  dzParser
import time




async def traverse():
    count = 0
    start_time = time.time()
    categories = dzParser.parse_categorie_links()
    for cate in categories:
        prodlist = await dzParser.traverse_a_category(cate)
        for product in prodlist:
            qna_list = await  dzParser.parse_qna_product(product)
            count= count+ len(qna_list)
            print(f'Total {count} qna parsed')


        print("--- %s seconds ---" % (time.time() - start_time))

asyncio.run(traverse())


