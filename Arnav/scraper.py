import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd  # For data handling
import textstat
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure the VADER lexicon is downloaded
nltk.download('vader_lexicon')

# Function to extract text chunks from the webpage, clean them, and compute readability and sentiment statistics
def fetch_and_analyze_readability(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        page = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page {url}: {e}")
        return pd.DataFrame()  # Return empty DataFrame

    # Parse the HTML page
    soup = BeautifulSoup(page, "lxml")

    # Remove unwanted elements like scripts, styles, and comments
    for script in soup(["script", "style", "noscript"]):
        script.extract()  # Remove these elements from the soup

    # Remove HTML comments
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Extract text chunks from paragraphs and headings
    text_chunks = []
    for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        text = element.get_text(strip=True)
        if text:  # Ensure it's not empty
            text_chunks.append(text)

    # Initialize sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # List to store results
    results = []

    # For each text chunk, compute statistics and sentiment
    for chunk in text_chunks:
        stats = compute_statistics(chunk)
        sentiment = sid.polarity_scores(chunk)
        # Determine sentiment category
        if sentiment['compound'] >= 0.05:
            sentiment_category = 'Positive'
        elif sentiment['compound'] <= -0.05:
            sentiment_category = 'Negative'
        else:
            sentiment_category = 'Neutral'
        # Combine all results into a dictionary
        result = {'URL': url, 'Text Chunk': chunk}
        result.update(stats)
        result['Sentiment'] = sentiment_category
        results.append(result)

    # Create DataFrame from results
    df = pd.DataFrame(results)
    return df

# Function to compute readability scores using textstat
def compute_statistics(text):
    stats = {}
    # Calculate various readability metrics
    stats['Flesch Reading Ease'] = textstat.flesch_reading_ease(text)
    stats['Flesch-Kincaid Grade Level'] = textstat.flesch_kincaid_grade(text)
    stats['SMOG Index'] = textstat.smog_index(text)
    stats['Gunning Fog Index'] = textstat.gunning_fog(text)
    stats['Automated Readability Index'] = textstat.automated_readability_index(text)
    stats['Coleman Liau Index'] = textstat.coleman_liau_index(text)
    stats['Dale-Chall Readability Score'] = textstat.dale_chall_readability_score(text)
    stats['Linsear Write Formula'] = textstat.linsear_write_formula(text)
    stats['Difficult Words'] = textstat.difficult_words(text)
    stats['Total Number of Sentences'] = textstat.sentence_count(text)
    stats['Total Number of Words'] = textstat.lexicon_count(text)
    return stats

# Function to read URLs from a newline-separated file and analyze each one
def analyze_urls_from_file(filename):
    # Read the file and extract URLs
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Error reading the file: {e}")
        return

    # Initialize an empty list to collect DataFrames
    all_results = []

    # Iterate over each URL and analyze readability
    for index, url in enumerate(urls):
        print(f"Processing URL {index + 1}: {url}")
        df = fetch_and_analyze_readability(url)
        if not df.empty:
            all_results.append(df)

    # Concatenate all DataFrames
    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        # Output the DataFrame into a markdown file
        final_df.to_markdown('readability_analysis.md', index=False)
        print("Analysis complete. Results saved to 'readability_analysis.md'.")
    else:
        print("No results to display.")

# Example of running the analysis with a file
filename = input("Please provide a filename containing URLs: ")  # Path to the file containing the URLs
analyze_urls_from_file(filename)


