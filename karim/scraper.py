import requests
from bs4 import BeautifulSoup, Comment
import textstat  # Readability analysis library
import pandas as pd  # For reading the CSV file

# Function to extract text from the webpage, clean it, and compute readability statistics
def fetch_and_analyze_readability(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        page = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page {url}: {e}")
        return
    
    # Parse the HTML page
    soup = BeautifulSoup(page, "lxml")
    
    # Remove unwanted elements like scripts, styles, and comments
    for script in soup(["script", "style", "noscript"]):
        script.extract()  # Remove these elements from the soup
        
    # Remove HTML comments
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    # Extract all visible text from the page
    text = ' '.join(soup.stripped_strings)  # Join all the lines into a single string
    
    # Analyze readability statistics using textstat
    analyze_readability(text, url)

# Function to compute readability scores using textstat
def analyze_readability(text, url):
    # Calculate and print various readability metrics
    print(f"Readability Analysis of the Webpage: {url}")
    print("-" * 40)
    print(f"Flesch Reading Ease: {textstat.flesch_reading_ease(text):.2f}")
    print(f"Flesch-Kincaid Grade Level: {textstat.flesch_kincaid_grade(text):.2f}")
    print(f"SMOG Index: {textstat.smog_index(text):.2f}")
    print(f"Gunning Fog Index: {textstat.gunning_fog(text):.2f}")
    print(f"Automated Readability Index: {textstat.automated_readability_index(text):.2f}")
    print(f"COLEMAN LIAU Index: {textstat.coleman_liau_index(text):.2f}")
    print(f"Dale-Chall Readability Score: {textstat.dale_chall_readability_score(text):.2f}")
    print(f"Linsear Write Formula: {textstat.linsear_write_formula(text):.2f}")
    print(f"Difficult Words: {textstat.difficult_words(text)}")
    print(f"Total Number of Sentences: {textstat.sentence_count(text)}")
    print(f"Total Number of Words: {textstat.lexicon_count(text)}")
    print("-" * 40)

# Function to read URLs from CSV and analyze each one
def analyze_urls_from_csv(csv_file):
    # Read the CSV file into a DataFrame
    try:
        urls_df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return
    
    # Assuming the URLs are in a column called 'URL'
    if 'URL' not in urls_df.columns:
        print("The CSV file must have a 'URL' column.")
        return
    
    # Iterate over each URL and analyze readability
    for index, row in urls_df.iterrows():
        url = row['URL']
        print(f"Processing URL {index + 1}: {url}")
        fetch_and_analyze_readability(url)

# Example of running the analysis with a CSV file
csv_file = input("Please provide a CSV filename: ")  # Path to the CSV file containing the URLs
analyze_urls_from_csv(csv_file)

