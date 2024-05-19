import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
import time
from urllib.robotparser import RobotFileParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_url(url):
    parsed_url = urllib.parse.urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)

def fetch_url_content(url):
    try:
        if not is_valid_url(url):
            logging.error("Invalid URL format. Please include a valid scheme (http or https).")
            return "Invalid URL format. Please include a valid scheme (http or https)."

        if not is_allowed_by_robots(url):
            logging.warning("URL is disallowed by robots.txt.")
            return "Access to this URL is disallowed by robots.txt."

        headers = {'User-Agent': 'Mozilla/5.0 (compatible; WebCrawler/1.0)'}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.find('title')
            page_title = title.text.strip() if title else "No title found"
            
            paragraphs = soup.find_all('p')
            
            content = "\n".join([p.get_text(strip=True) for p in paragraphs])
            
            return f"**Page Title:** {page_title}\n\n**Content:**\n{content}"
        else:
            logging.error(f"Failed to retrieve URL. HTTP Status Code: {response.status_code}")
            return f"Failed to retrieve URL. HTTP Status Code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return f"An error occurred: {e}"

def is_allowed_by_robots(url):
    parsed_url = urllib.parse.urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch('*', url)

def main():
    while True:
        url = input("Enter the URL (or type 'exit' to quit): ")
        if url.lower() == 'exit':
            logging.info("Exiting the URL fetcher.")
            break
        logging.info(f"Fetching content from URL: {url}")
        content = fetch_url_content(url)
        
        print(content)
        time.sleep(1) 

if __name__ == "__main__":
    main()
