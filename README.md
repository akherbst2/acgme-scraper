# acgme-scraper

Goal:  Scrape search results from https://apps.acgme.org/ads/Public/Programs/Search.
Scraper will search for results in NY state.  Then, it will grab the search result 10-digit ID number (i.e. 0200121109 for university of alabama medical center program), the title of the page, (i.e. "UNIVERSITY OF ALABAMA MEDICAL CENTER PROGRAM"), the number of "Total Approved Resident Positions", and the total of "Total Filled Resident Positions".  It will output results to `results.csv`, which can be viewed/edited in a spreadsheet.

NOTE: Any urls that could not be read by the scraper will be output to `errors.txt`.  You will have to process this data manually.


# Quick Start

Install requirements

` pip install -r requirements.txt`

Run scraper

` python scraper.py`

See results in `results.csv`.  See urls that errored in `errors.txt`.
