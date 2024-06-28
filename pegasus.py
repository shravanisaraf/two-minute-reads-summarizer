'''pegasus --> 1 min 30 seconds'''
import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
import time
from urllib.robotparser import RobotFileParser
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Summarization function using Pegasus
def summarize_text(text):
    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    summary_ids = model.generate(tokens["input_ids"], max_length=60, num_beams=4, length_penalty=2.0, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# URL validation
def is_valid_url(url):
    parsed_url = urllib.parse.urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)

# Fetch URL content
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

# Check robots.txt permissions
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

        if "Content" in content:
            start_idx = content.find("**Content:**") + len("**Content:**\n")
            text_content = content[start_idx:]
            summary = summarize_text(text_content)
            print(f"Summary:\n{summary}")
        else:
            print(content)

        time.sleep(1)

if __name__ == "__main__":
    main()
