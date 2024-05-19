# 2 Minute Reads: An Article Summarizer

## Overview

This project is an article summarizer that takes user input in the form of URLs and documents. It then extracts the text content from the URLs and summarizes it using a pre-trained T5 model from the Hugging Face Transformers library. The application is built with a backend server using Flask and a simple frontend UI using HTML, CSS, and JavaScript.

## Features

- **Web Crawler**: Uses BeautifulSoup to crawl web pages based on user input and collect relevant URLs.
- **Content Parsing**: Extracts text content from the collected URLs.
- **Text Summarization**: Implements a basic text summarization model using a pre-trained T5 model. Fine-tuning is optional.
- **Backend**: Flask server to handle user input, trigger the web crawler, and process the summarization.
- **Frontend**: Simple user interface for entering search strings and viewing summarized results.

## Web Crawler

The web crawler is implemented using BeautifulSoup. It:

- Accepts user input to search the web.
- Collects URLs of relevant articles.
- Extracts text content from these URLs.

## Text Summarization

The text summarization feature uses a pre-trained T5 model from the Hugging Face Transformers library. It:

- Loads the pre-trained T5 model.
- Summarizes the extracted text content.

## Backend

The backend is built using Flask. It:

- Handles user input.
- Triggers the web crawler.
- Processes the text summarization.

## Frontend

The frontend provides a user-friendly interface for:

- Entering a search string.
- Viewing the summarized results.

It is built using HTML, CSS, and JavaScript. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
