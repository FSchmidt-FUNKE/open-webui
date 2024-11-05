# -*- coding: utf-8 -*-
"""
Created on Okt 31 15:31:07 2024

@author: friedrich.schmidt
"""

import logging
from typing import Optional

import requests
from open_webui.apps.retrieval.web.main import SearchResult, get_filtered_results
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


def search_bing(
    api_key: str, query: str, count: int, filter_list: Optional[list[str]] = None
) -> list[SearchResult]:
    """Search using Bing's Search API and return the results as a list of SearchResult objects.

    Args:
        api_key (str): A Bing Search API key
        query (str): The query to search for
        count (int): The number of results to return
        filter_list (Optional[list[str]]): A list of strings to filter the search results
    """
    url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": api_key }
    params = {"q": query, "mkt": "de-DE", "responseFilter": "Webpages", 'count': count , 'offset': 0}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    json_response = response.json()
    results = json_response.get("webPages", {}).get("value", [])
    if filter_list:
        results = get_filtered_results(results, filter_list)

    return [
        SearchResult(
            link=result["url"], title=result.get("title"), snippet=result.get("snippet")
        )
        for result in results[:count]
    ]