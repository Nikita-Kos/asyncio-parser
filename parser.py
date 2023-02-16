import aiohttp
import asyncio
import requests
from bs4 import BeautifulSoup

category_lst = []
pagen_lst = []
domain = 'https://parsinger.ru/asyncio/create_soup/1/'
z = []

def get_soup(url):
    resp = requests.get(url=url)
    return BeautifulSoup(resp.text, 'lxml')


def get_urls_categories(soup):
    all_link = soup.find('div', class_='item_card').find_all('a')

    for cat in all_link:
        category_lst.append(domain + cat['href'])


def get_urls_pages(category_lst):
    for cat in category_lst:
        resp = requests.get(url=cat)
        soup = BeautifulSoup(resp.text, 'lxml')
        for pagen in soup.find('div', class_='pagen').find_all('a'):
            pagen_lst.append(domain + pagen['href'])


async def get_data(session, link):
    async with session.get(url=link) as response:
        resp = await response.text()
        soup = BeautifulSoup(resp, 'lxml')
        item_card = soup.find('div', class_='item_card')
        if item_card:
            z.append(int(item_card.text))

async def main():
     async with aiohttp.ClientSession() as session:
         tasks = []
         for link in category_lst:
             task = asyncio.create_task(get_data(session, link))
             tasks.append(task)
         await asyncio.gather(*tasks)


url = 'https://parsinger.ru/asyncio/create_soup/1/index.html'
soup = get_soup(url)
get_urls_categories(soup)

asyncio.run(main())
print(sum(z))