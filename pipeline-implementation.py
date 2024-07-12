import requests
from transformers import pipeline

# Available summarization models
summarization_models = {
    "1": "facebook/bart-large-cnn",
    "2": "t5-small",
    "3": "t5-base",
    "4": "t5-large",
    "5": "google/pegasus-xsum",
    "6": "MeaningCloud API"
}

def display_menu():
    print("Choose a summarization model:")
    print("1: BART (facebook/bart-large-cnn)")
    print("2: T5 Small (t5-small)")
    print("3: T5 Base (t5-base)")
    print("4: T5 Large (t5-large)")
    print("5: Pegasus (google/pegasus-xsum)")
    print("6: MeaningCloud API")

def summarize_with_transformer(model_name, text):
    summarizer = pipeline("summarization", model=model_name)
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]['summary_text']

def summarize_with_meaningcloud(api_key, text):
    url = "https://api.meaningcloud.com/summarization-1.0"
    payload = {
        'key': api_key,
        'txt': text,
        'sentences': 5
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get('summary', 'No summary available')
    else:
        return 'Error: Unable to summarize text using MeaningCloud API'

def main():
    display_menu()
    choice = input("Enter the number of the model you want to use: ")

    if choice in summarization_models:
        text = input("Enter the text you want to summarize (up to 50,000 characters for MeaningCloud, shorter for models like BART and T5): ")

        if choice == "6":
            api_key = 'ec3f917dddbb78cc4915da35f54a1ef3'  
            print("\nSummarizing using MeaningCloud API")
            summary = summarize_with_meaningcloud(api_key, text)
        else:
            model_name = summarization_models[choice]
            print(f"\nSummarizing using model: {model_name}")
            summary = summarize_with_transformer(model_name, text)

        print("\nSummary:")
        print(summary)
    else:
        print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
