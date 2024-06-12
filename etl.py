import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import json

# Download NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')



def preprocess_text(text):
    # Tokenization
    tokens = word_tokenize(text)
    
    # Lowercasing
    tokens = [token.lower() for token in tokens]
    
    # Removing punctuation and non-alphanumeric characters
    tokens = [token for token in tokens if token.isalnum()]
    
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    
    # Joining tokens back into a string
    processed_text = ' '.join(tokens)
    
    return processed_text


def extract_dawn():
    # URL of the LinkedIn job listings page
    url = "https://www.dawn.com"



    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")



    #finding link towards the sports page
    links = [link['href'] for link in soup.find_all("a")]
    # print(links)


    #fethcing the article links
    article_links = [link for link in links if "/news/" in link]
    # print(article_links)


    # Initialize a list to store the content of each article
    article_contents = []

    # Iterate over each article URL
    for url in article_links[:10]:
        # Send a GET request to the URL to fetch the HTML content
        response = requests.get(url)
        print(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the content of the article (assuming it's in a <div> with class="entry-content" or similar)
            heading = soup.find('h2').get_text()
            content=soup.find('div', class_='story__content').get_text()


            heading=preprocess_text(heading)
            content=preprocess_text(content)
            dic={}
            dic[heading]=content
            # Append the article content to the list
            # article_contents.append(article_content)
        else:
            print(f"Failed to retrieve content from {url}")

    # Print or process the extracted article contents
    # print(dic)

    return dic

def extract_bbc():
     # URL of the LinkedIn job listings page
    url = "https://www.bbc.com/"



    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")



    #finding link towards the sports page
    links = [link['href'] for link in soup.find_all("a")]
    # print(links)


    article_links = [url for url in links if '/article/' in url]

    for url in article_links[:10]:
        # Send a GET request to the URL to fetch the HTML content
        url="https://www.bbc.com" + url
        response = requests.get(url)
        print(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the content of the article (assuming it's in a <div> with class="entry-content" or similar)
            heading = soup.find('h1').get_text()
            contents = soup.find_all('div', {'data-component': 'text-block'})
            content=""
            for c in contents:
                content=content+ '--' + c.get_text()

            heading=preprocess_text(heading)
            content=preprocess_text(content)
            dic={}
            dic[heading]=content
            # Append the article content to the list
            # article_contents.append(article_content)
        else:
            print(f"Failed to retrieve content from {url}")

    # Print or process the extracted article contents
    # print(dic)

    return dic




def extract():
    bbc = extract_bbc()
    dawn = extract_dawn()

    return bbc, dawn

def load(bbc, dawn):
    with open('dawn.json', 'w') as file:
            json.dump(dawn, file, indent=4)
    with open('bbc.json', 'w') as file:
            json.dump(bbc, file, indent=4)



bbc, dawn = extract()

load(bbc, dawn)

