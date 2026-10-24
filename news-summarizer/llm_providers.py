import os

import cohere
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

cohere_api_key = os.getenv("COHERE_API_KEY")
if cohere_api_key:
    cohere_client = cohere.ClientV2(api_key=cohere_api_key)
else:
    cohere_client = None


def summarize_with_openai(article_text):
    """Summarize an article with OpenAI."""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize the news article in 2-3 clear sentences.",
            },
            {
                "role": "user",
                "content": article_text,
            },
        ],
    )

    summary = response.choices[0].message.content
    usage = response.usage

    return {
        "text": summary,
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
    }


def analyze_sentiment_with_cohere(article_text):
    """Analyze an article's sentiment with Cohere."""
    if cohere_client is None:
        raise ValueError("COHERE_API_KEY is missing from the .env file")

    response = cohere_client.chat(
        model="command-r-plus-08-2024",
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the sentiment of the news article as "
                    "positive, negative, or neutral. Give one short reason."
                ),
            },
            {
                "role": "user",
                "content": article_text,
            },
        ],
    )

    return response.message.content[0].text


def analyze_sentiment_with_fallback(article_text):
    """Try Cohere first; use OpenAI if Cohere fails."""
    try:
        return {
            "provider": "Cohere",
            "sentiment": analyze_sentiment_with_cohere(article_text),
        }
    except Exception as error:
        print(f"Cohere failed; using OpenAI instead. Reason: {error}")

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Classify the sentiment as positive, negative, or "
                        "neutral. Give one short reason."
                    ),
                },
                {
                    "role": "user",
                    "content": article_text,
                },
            ],
        )

        return {
            "provider": "OpenAI fallback",
            "sentiment": response.choices[0].message.content,
        }


if __name__ == "__main__":
    test_text = (
        "A technology company announced a new product that received "
        "positive reviews from customers."
    )

    summary_result = summarize_with_openai(test_text)
    print("Summary:", summary_result["text"])
    print("OpenAI tokens:", summary_result["input_tokens"],
          "input,", summary_result["output_tokens"], "output")

    sentiment_result = analyze_sentiment_with_fallback(test_text)
    print("Sentiment provider:", sentiment_result["provider"])
    print("Sentiment:", sentiment_result["sentiment"])