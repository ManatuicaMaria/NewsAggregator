from django.shortcuts import render
from esutils.search import search as elastic_search

class Article:
    
    def __init__(self, title, description, date, author, url, real_degree, pa_fake, svc_fake):
        self.title = title
        self.description = description
        self.date = date
        self.author = author
        self.url = url
        self.real_degree = real_degree
        self.pa_fake = pa_fake
        self.svc_fake = svc_fake

def search(request):
    if 'query' in request.GET:
        # TODO: paginare sau maxim 30 entries
        query = request.GET['query']
        results = elastic_search(query)
        articles = [Article(**results["hits"][i]['_source']) for i in range(results["total"])]
        
        # Used for debuging
        # articles = [Article("title", "description", "18-11-2018", "Teo", "https://google.com" , 60, True, False)]
        return render(request, 'list.html', {'articles': articles, 'query': query })
    else:
        return render(request, 'list.html')