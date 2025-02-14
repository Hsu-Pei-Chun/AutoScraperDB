from config.config import USER_AGENTS
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

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    test_url = "https://www.vscinemas.com.tw/vsweb/film/index.aspx"
    page_content = fetch_page(test_url)

    if page_content:
        print("成功獲取網頁內容")
        print(page_content[:500])  # 只顯示前 500 個字元，避免輸出太多
    else:
        print("獲取網頁內容失敗")