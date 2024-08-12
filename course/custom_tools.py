""" Custom tools definition """
from typing import List, Dict
from duckduckgo_search import DDGS
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup


class SearchTools:
    @tool("Web search")
    @staticmethod
    def web_search(keywords: str) -> List[Dict[str, str]]:
        """ Search the web using keywords in one string input variable and obtain a list of URLs """
        ddgs = DDGS()

        results = ddgs.text(keywords=keywords, max_results=10)
        return results


class SearchSpecificWebsites:
    @tool("Web search on specific websites")
    @staticmethod
    def web_search_specific_websites(country: str) -> str:
        """ Search the web using a specific website """
        return f"https://results.elections.europa.eu/en/{country.lower()}/"


class WebScraper:
    @tool("Web scraping for specific section")
    @staticmethod
    def web_scraping_specific_section(url) -> str:
        """ Scrape specific part of the website """
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            html_content = response.content
        else:
            print(f"Failed to retrieve content. Status code: {response.status_code}")
        soup = BeautifulSoup(html_content, 'lxml', from_encoding='utf-8')
        specific_element = soup.find('section', id='country-view-results')
        return specific_element

