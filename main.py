
from scraper import scrape

if __name__ == '__main__':

    # Scrape Google Scholar for metaheuristics articles published in 2024
    results = scrape("metaheuristics", 
                     nb_pages=1, 
                     year=2024,
                     save_to_file=True)

    print("All done!")
