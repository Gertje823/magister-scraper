# Magister-Scraper
This is a script to download your Magister data.

## How to use
Login to your magister account in the browser. Open the developer tools (f12) and look for any api request. Copy the Bearer token from the request header into the script (line 5). And edit the base url (line 3).
Run the script `python3 magister.py`

## Data that will be scraped
After you run the script, there will be 3 json files for each year.
`Absenties`, `Cijfers` and `Rooster`


##  Feature requests
If you have any feature requests don't hesitate to open a issue :)