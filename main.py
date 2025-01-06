
# External libraries
import time

# Internal libraries
from scraper import scrape
from downloader import download_from_json


if __name__ == '__main__':

    # Iterate over years from 2001 to 2024
    for year in range(2001, 2025):

        # Retry up to n times if an error occurs
        for attempt in range(1, 3):
            
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
                    print(f"Failed to process year {year} after 3 attempts.")

                # Wait one minute
                time.sleep(60)

    print("All done!")
