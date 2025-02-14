from config.config import USER_AGENTS
from .parser import get_last_page
import random
import requests
import time
import logging

def fetch_page(url, retries = 3):
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    for i in range(retries):
        try:
            logging.info(f"Fetching URL: {url} (嘗試 {i+1}/{retries})")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.error(f"Failed to fetch {url}: {e}")
        time.sleep(5)
    return None


def fetch_all_pages(base_url):
    first_page_content = fetch_page(f"{base_url}?p=1")

    if not first_page_content:
        logging.error("無法獲取首頁內容，終止爬取")
        return []
    
    last_page = get_last_page(first_page_content)
    all_data = []

    for page in range(1, last_page + 1):
        url = f"{base_url}?p={page}"
        page_content = fetch_page(url)

        if not page_content:
            logging.error(f"無法獲取頁面 {url} 的內容")
            continue

        logging.info(f"正在解析第 {page} 頁")
        all_data.append(page_content)
        time.sleep(2)

    return all_data



if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    base_url = "https://www.vscinemas.com.tw/vsweb/film/index.aspx"
    pages_content = fetch_all_pages(base_url)

    logging.info(f"共抓取了 {len(pages_content)} 頁")