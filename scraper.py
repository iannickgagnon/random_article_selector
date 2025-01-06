
# External libraries
import os
import json
import requests
from bs4 import BeautifulSoup
from habanero import Crossref


def scrape(query: str, 
           nb_pages: int, 
           year: int = None,
           save_to_file: bool = False) -> list:
    """
    Scrapes Google Scholar search results for a specified query and number of pages, 
    optionally filtering by publication year. Fetches DOIs using the CrossRef API 
    of the habanero library.

    Args:
        query (str): The search query string.
        nb_pages (int): The number of pages to scrape from Google Scholar.
        year (int, optional): The publication year to filter results by. Defaults to None.
        save_to_file (bool, optional): Whether to save the scraped results to a text file. Defaults to False.

    Returns:
        list: A list of dictionaries, each containing:
            - 'title': The title of the article.
            - 'link': The link to the article.
            - 'doi': The DOI of the article, if available.
    """
    
    # The number of results shown on each page
    NB_RESULTS_PER_PAGE = 10
    
    # Custom headers to mimic browser behavior
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
    }
    
    # Initialize session
    session = requests.Session()
    session.headers.update(headers)
    
    # Initialize Crossref instance
    cr = Crossref()
    
    # Initialize container for output articles
    articles = []
    
    # Iterate through each page's articles
    for page_index in range(nb_pages):
        # Results iterator
        start_index = page_index * NB_RESULTS_PER_PAGE
        
        # Build URL with query and year filter
        url = f"https://scholar.google.com/scholar?q={query}&hl=en&start={start_index}"
        if year:
            url += f"&as_ylo={year}&as_yhi={year}"
        
        # Send HTTP request
        response = session.get(url)
        response.raise_for_status()
        
        # Parse HTTP request response as HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        for result in soup.find_all('div', class_='gs_ri'):

            # Get title
            title_tag = result.find('h3', class_='gs_rt')
            title = title_tag.get_text() if title_tag else None
            
            # Get the href attribute from the hyperlink
            link_tag = result.find('a')
            link = link_tag['href'] if link_tag else None
            
            # Validate the title and link
            if not title or not link or not link.startswith('http'):
                print(f"Skipping invalid entry: Title: {title}, Link: {link}")
                continue
            
            # Attempt to fetch DOI using habanero
            doi = None
            try:
                search_results = cr.works(query=title)
                if search_results['message']['items']:
                    doi = search_results['message']['items'][0].get('DOI')
            except Exception as e:
                print(f"Error fetching DOI for title '{title}': {e}")
            
            # Save article as dictionary (without authors)
            article = {
                'title': title,
                'link': link,
                'doi': doi
            }

            # Store article in output list
            articles.append(article)
    
       # Save results to file
    if save_to_file:

        # Default filename
        if year:
            filename = f"{query}_{year}_results.json"
        else:
            filename = f"{query}_results.json"

        # Make sure the filename is unique
        i = 1
        while os.path.exists(filename):
            filename = f"{query}_results_{i}.json"
            i += 1
    
        # Write to a JSON file
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(articles, file, ensure_ascii=False, indent=4)

    return articles
