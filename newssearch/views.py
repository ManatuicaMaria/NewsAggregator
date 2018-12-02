from django.shortcuts import render
from esutils.search import search as elastic_search

PAGE_SIZE=30

class Article:
    
    def __init__(self, title, description, content, date, author, url, real_degree, pa_fake, svc_fake):
        self.title = title
        self.description = description
        self.content = content
        self.date = date
        self.author = author
        self.url = url
        self.real_degree = real_degree
        self.pa_fake = pa_fake
        self.svc_fake = svc_fake

def search(request):
    if 'query' in request.GET:
        # TODO: paginare
        # TODO: highlights
        query = request.GET['query']
        results = elastic_search(query, results_number=PAGE_SIZE, starting_position=0)
        articles = [Article(**results["hits"][i]['_source']["doc"]) for i in range(PAGE_SIZE)]
        
        # Used for debuging
        # articles = [Article("title", "description", "18-11-2018", "Teo", "https://google.com" , 60, True, False)]
        return render(request, 'list.html', {'articles': articles, 'query': query })
    else:
        return render(request, 'list.html')