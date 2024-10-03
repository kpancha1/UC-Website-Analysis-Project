import requests
from bs4 import BeautifulSoup

#Function to get only paragraph text on a website
def p_scrapper(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text from all paragraphs on the page
        paragraphs = soup.find_all('p')
        
        # Concatenate the text from all paragraphs
        scraped_text = '\n'.join([p.get_text() for p in paragraphs])
        
        # Output the scraped text in the terminal
        print(scraped_text)
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)


# Example usage:
url = 'https://www.math.ucsb.edu/about'  # Replace with your desired URL
p_scrapper(url)


#Function to get ALL text from a webstie
def all_scrapper(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text from all paragraphs on the page
        all_text = soup.get_text(separator='\n', strip=True)
        
        # Output the scraped text in the terminal
        print(all_text)
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)


# Example usage:
url = 'https://www.math.ucsb.edu/about'  # Replace with your desired URL
all_scrapper(url)