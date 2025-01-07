
# External libraries
import os
import re
import json
import time
import requests


def download(doi: str, 
             output_folder: str,
             max_size: int = 5):
    """
    Downloads a PDF article from a DOI-based URL, with an optional size limit.

    Args:
        doi (str): The DOI of the article to download.
        output_folder (str): The folder where the downloaded PDF will be saved.
        max_size (int, optional): The maximum allowed size of the file in MB. Defaults to 5 MB.

    Returns:
        str: A message indicating success or failure of the download.
    """

    # Build the URL from the DOI
    pdf_url = f"https://sci.bban.top/pdf/{doi}.pdf"

    # Create destination folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f"{doi_to_filename(doi)}.pdf")

    # Headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://www.wellesu.com/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-CH-UA": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "Windows",
    }

    try:

        # Send a GET request to download the PDF
        response = requests.get(pdf_url, headers=headers, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            
            # Get content length from headers (if provided)
            content_length = response.headers.get("Content-Length")
            if content_length:
                size_in_mb = int(content_length) / (1_048_576)  # Bytes -> Megabytes
                if size_in_mb > max_size:
                    print(f"File size {size_in_mb:.2f} MB exceeds the maximum allowed size of {max_size} MB. Download aborted.")
                    return

            # Write the content to a file
            with open(output_file, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return
        else:
            print(f"Failed to download the PDF. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


def doi_to_filename(doi: str) -> str:
    """
    Transforms a DOI into a filesystem-safe filename by replacing '.', '/' and other unsafe characters with '_'.

    Args:
        doi (str): The DOI to transform.

    Returns:
        str: A transformed, filesystem-safe filename.
    """
    # Replace unsafe characters (., /) with underscores
    filename = re.sub(r'[./-]', '_', doi)
    return filename


def download_from_json(file_path: str,
                       output_folder: str, 
                       max_size: int = 5):
    """
    Reads a JSON file containing article data and downloads all articles.

    Args:
        file_path (str): The path to the JSON file containing article data.
        output_folder (str): The folder where the downloaded PDFs will be saved.
        max_size (int, optional): The maximum allowed size of each file in MB. Defaults to 5 MB.

    Returns:
        None
    """
    try:

        # Load articles from JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            articles = json.load(file)

        # Iterate through each article and download its PDF
        for article in articles:
            doi = article.get('doi')
            if doi:
                print(f"Downloading article with DOI: {doi}")
                download(doi, output_folder, max_size=max_size)
            
                # Wait to avoid 429 error (too many requests)
                time.sleep(5)
            
            else:
                print(f"Skipping article without DOI: {article.get('title', 'Unknown title')}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file '{file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
