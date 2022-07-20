import asyncio
import requests
import aiohttp
from bs4 import BeautifulSoup as soup
import json

daraz_main_link = "https://www.daraz.com.bd"


def parse_url_synchonousely(url):
    req = requests.get(url)
    return req.content


async def parse_url_async(url):
    async with aiohttp.ClientSession(trust_env=True) as session:
        response = await session.get(url, ssl=False)
        html = await response.text()
        return html


async def parse_qna_product(product_link):
    qna_list = []
    html = await parse_url_async(product_link)
    sp = soup(html, 'html.parser')
    for script in sp.find_all("script"):
        script_tag = script.getText().strip()
        if script_tag.startswith('window.LZD_RETCODE_PAGENAME'):
            qna_json = script_tag.split("app.run(")[1].split(");")[0]
            if qna_json is not None:
                try:
                    qna_dict = json.loads(qna_json)
                    qna_items = qna_dict["data"]["root"]["fields"]["qna"]["items"]
                    for qna in qna_items:
                        qna_list.append(qna)
                except Exception as e:
                    print(f'Exception: No Qna found ')
                    continue
    return qna_list


def parse_categorie_links():
    html = parse_url_synchonousely(daraz_main_link)
    sp = soup(html, 'html.parser')
    categories = sp.find_all('li', class_='lzd-site-menu-grand-item')
    categories_links = []
    for li in categories:
        link = li.a.get('href')
        link = f"https:{link}"
        categories_links.append(link)
    return categories_links


def add_pagination_pages(product_available, cate_link):
    new_pages = []
    if product_available is not None:
        try:
            product_available = int(int(product_available) / 40)

            if product_available > 60:
                product_available = 60
            for i in range(product_available):
                new_page_link = f"https://{cate_link}?page={i}"
                new_pages.append(new_page_link)
        except Exception as e:
            print('exception: {e}')
            return new_pages
    return new_pages


async def traverse_a_category(category_link):
    category_pages = [category_link]
    product_links = []
    print(f'Traversing a category: {category_link}')

    for cate_link in category_pages:
        print(type(cate_link))
        html = await parse_url_async(cate_link)

        cate_html = soup(html, 'html.parser')
        for data in cate_html.find_all("script"):
            text = data.getText()
            if text.startswith('window.pageData'):
                page_content = text.split(".pageData=")[1]
                if page_content is None:
                    continue
                try:
                    json_content = json.loads(page_content)
                except:
                    continue
                try:
                    all_showed_product = json_content["mods"]["listItems"]
                except:
                    continue
                for prod in all_showed_product:
                    product_links.append("https:" + prod["productUrl"])

        if '?page=' not in cate_link:
            available_prod = json_content["mods"]["resultTips"]["tips"].split(" items found")[0]
            new_pages = add_pagination_pages(available_prod, cate_link)
            category_pages = category_pages + new_pages
    return product_links
