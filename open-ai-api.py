import requests
from bs4 import BeautifulSoup
import openai

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

def extract_content_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # This example assumes the main content is within <p> tags
    paragraphs = soup.find_all('p')
    article_content = ' '.join([p.get_text() for p in paragraphs])

    return article_content

def summarize_content(content, max_tokens=150):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following article: {content}",
        max_tokens=max_tokens,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()
    return summary

def main():
    url = input("Enter the URL of the article you want to summarize: ")
    article_content = extract_content_from_url(url)
    print("\nOriginal Article Content:\n", article_content)

    summary = summarize_content(article_content)
    print("\nSummarized Article:\n", summary)

if __name__ == "__main__":
    main()
