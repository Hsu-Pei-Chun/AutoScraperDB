from bs4 import BeautifulSoup
import logging

def get_last_page(html):
    soup = BeautifulSoup(html, "lxml")
    pagebar = soup.find("section", class_="pagebar")

    if not pagebar:
        logging.error("找不到 pagebar，可能是網頁結構有變動")
        return 1
    
    page_links = pagebar.find_all("a")
    page_numbers = []

    for link in page_links:
        href = link.get("href", "")
        if "?p=" in href:
            try:
                page_num = int(href.split("?p=")[-1])
                page_numbers.append(page_num)
            except ValueError:
                continue
    
    if page_numbers:
        last_page = max(page_numbers)
        logging.info(f"找到最後一頁: {last_page}")
        return last_page
    else:
        logging.error("未解析出任何頁數")
        return 1