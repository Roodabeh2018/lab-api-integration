## Execution trace
Command: `python main.py`

The program successfully fetched three technology news articles, summarized them with OpenAI, and analyzed their sentiment with Cohere. The terminal displayed the title, source, summary, sentiment, provider, and URL for each article.

Test command: `pytest test_summarizer.py -v`

Result: 2 tests passed.

## Output record

- Title: Dell releases new 16-inch laptop globally with 1,600-nit OLED display and up to 128 GB RAM - Notebookcheck
- Source: Notebookcheck.net
- Summary: The 20-core version of the RTX Spark N1X, featuring a 6,144-core GPU, is now available with 1 TB of storage.
- Sentiment: Neutral
- Sentiment provider: Cohere
- URL: https://www.notebookcheck.net/Dell-releases-new-16-inch-laptop-globally-with-1-600-nit-OLED-display-and-up-to-128-GB-RAM.1431301.0.html

## Limitation or failure risk

If an article has no text, the program skips it. If an API key is missing or a provider is unavailable, the workflow may stop or use its fallback provider.