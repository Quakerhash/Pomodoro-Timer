from django.shortcuts import render
from django.http import HttpResponse
import requests
import os


API_KEY = os.environ.get('API_KEY')
SEARCH_ENGINE_ID = os.environ.get('SEARCH_ENGINE_ID')
url = 'https://www.googleapis.com/customsearch/v1'

def fetch_results(search_query, site_filter=None):
    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
    }
    if site_filter:
        params['siteSearch'] = site_filter 
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json()
        return [item["link"] for item in results.get("items", [])]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

def Learn(request):
    website_links = []
    youtube_links = []
    if request.method == "POST":
        search_query = request.POST.get("Topic", "").strip()
        if search_query:
            website_links = fetch_results(search_query)
            youtube_links = fetch_results(search_query, site_filter="youtube.com")
    return render(request, "learn.html", {
        "website_links": website_links,
        "youtube_links": youtube_links,
    })
