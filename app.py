from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
from urllib.robotparser import RobotFileParser
from transformers import BartTokenizer, BartForConditionalGeneration

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the BART tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

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

            # Summarize the content
            summarized_content = summarize_content(content)

            return {
                "page_title": page_title,
                "content": content,
                "summarized_content": summarized_content
            }
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

def summarize_content(content):
    try:
        inputs = tokenizer.encode("summarize: " + content, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summarized = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summarized
    except Exception as e:
        logging.error(f"An error occurred during summarization: {e}")
        return "An error occurred during summarization."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    content = fetch_url_content(url)
    return jsonify(content)

if __name__ == '__main__':
    app.run(debug=True)
