
from habanero import Crossref

cr = Crossref()
result = cr.works(query="A literature review and critical analysis of metaheuristics recently developed")
doi = result['message']['items'][0]['DOI']
print(f"DOI: {doi}")
