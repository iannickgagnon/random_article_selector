
# External libraries
import time

# Internal libraries
from scraper import scrape
from downloader import download_from_json
from analyzer import analyze_pdfs 

'''
**********
* CONFIG *
**********
'''

# Number of attempts to retry if an error occurs
NB_ATTEMPTS = 1

# Year range
YEAR_MIN = 2009
YEAR_MAX = 2025

if __name__ == '__main__':

    '''
    # Iterate over years from 2001 to 2024
    for year in range(YEAR_MIN, YEAR_MAX):

        # Retry up to NB_ATTEMPTS times if an error occurs
        for attempt in range(1, NB_ATTEMPTS + 1):
            
            try:

                # Scrape results and save to JSON file
                _ = scrape("metaheuristics", 
                           nb_pages=30, 
                           year=year,
                           save_to_file=True)

                # Download PDFs from JSON file
                download_from_json(f"metaheuristics_{year}_results.json", f"year_{year}")
                
                # Break out of the multi-attempt loop if successful
                break
            
            except Exception as e:
            
                # Print error message
                print(f"Attempt no.{attempt} failed for year {year}: {e}")
            
                # If the last attempt failed, print a message
                if attempt == 3:
                    print(f"Failed to process year {year} after {NB_ATTEMPTS} attempts.")

                # Wait one minute
                time.sleep(60)

    print("All done!")
    '''
    
    analyze_pdfs('test_1', 'test_1_results')
