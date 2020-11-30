# HackeroneScraper

## Welcome!
This tool scraps and categorises Hackerone's Hacktivity page for vulnerability reports. (Currently a terminal based tool) 

### Set up - Requirements
---
The following libraries are used to develop this tool

1. requests

	`pip install requests`
  
2. BeautifulSoup

	`pip install beautifulsoup`
  
3. selenium 

	`pip install selenium`  

4. termplotlib - https://github.com/nschloe/termplotlib

	`pip install termplotlib` 

### Usage
---
`python scrapper.py <seach keyword(s)>`

Example:

`python scrapper.py mobile application` 

### Capabilities

HackeroneScraper will do the following upon scraping the hacktivity query made.

1. Plot an ASCII bar graph. The graph will show the number of published/disclosed vulnerabilties for each Bug Bounty Program  