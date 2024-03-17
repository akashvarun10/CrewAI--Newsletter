import json
import os
from dotenv import load_dotenv
load_dotenv()

import requests
from langchain.tools import tool

class SearchTools():

  @tool("Search internet")
  def search_internet(query):
    """Useful to search the internet about a given topic and return relevant
    results."""
    print("Searching the internet...") 
    top_result_to_return = 5
    url = 'https://google.serper.dev/search'
    payload = json.dumps(
      {"q": query, "num": top_result_to_return,tbm:"nws"})
    headers = {
      'X-API-KEY': os.getenv['SERPER_API_KEY'],
      'content-type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if 'organic' not in response.json():
       return "Sorry, I couldn't find anything about that, there could be an error with y"
    else:
       results = response.json()['organic']
       string = []
       print ("Results:", results[:top_result_to_return])
       for result in results[:top_result_to_return]:
         try:
           # Attempt to extract the date
           date = result-get( 'date', 'Date not available')
           string.append('\n' . join([
               f"Title: {result['title']}",
               f"Link: {result['link']}",
               f"Date: {date}",
               f"Snippet: {result['snippet']}"
           ]))
         except KeyError:
           next
       return '\n'.join(string)
    
    
    
        

