'''T5---> 34 seconds'''
import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
import time
from urllib.robotparser import RobotFileParser
import transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration

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

# Load pre-trained T5 model for summarization
model_name = "t5-base"  # Adjust for different model sizes (e.g., "t5-small", "t5-large")
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def summarize_article(article_text, max_length=150, num_beams=5, no_repeat_ngram_size=3):
    """
    Summarizes an article using abstractive summarization with T5.

    Args:
        article_text (str): The text of the article to summarize.
        max_length (int): The maximum length of the generated summary (default: 150 words).
        num_beams (int): Number of beams for beam search (default: 5).
        no_repeat_ngram_size (int): Size of ngrams that should not be repeated in the summary (default: 3).

    Returns:
        str: The generated summary of the article.
    """
    try:
        # Preprocess text
        article_text = article_text.strip()  # Remove leading/trailing whitespace

        # Encode the article for T5
        inputs = tokenizer(article_text, return_tensors="pt", max_length=512, truncation=True)

        # Generate summary
        summary_ids = model.generate(
            **inputs, max_length=max_length, num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size, early_stopping=True
        )

        # Decode summary tokens back to text
        summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary_text

    except Exception as e:
        logging.error(f"An error occurred during summarization: {e}")
        return None

def main():
    while True:
        url = input("Enter the URL (or type 'exit' to quit): ")
        if url.lower() == 'exit':
            logging.info("Exiting the URL fetcher.")
            break
        logging.info(f"Fetching content from URL: {url}")
        content = fetch_url_content(url)

        if "Content:" in content:
            # Extract the actual content part for summarization
            content_text = content.split("**Content:**\n", 1)[-1]
            summary = summarize_article(content_text)
            print(f"Summary:\n{summary}")
        else:
            print(content)

        time.sleep(1)

if __name__ == "__main__":
    main()
