import math
from django.shortcuts import render
from esutils.search import search as elastic_search

PAGE_SIZE=10
DELTA=2
MIN_PAGE=1
class Article:
    
    def __init__(self, title, description, content, date, author, url, highlight, real_degree, pa_fake, svc_fake):
        self.title = title
        self.description = description
        self.content = content
        self.date = date
        self.author = author
        self.url = url
        self.real_degree = real_degree
        self.pa_fake = pa_fake
        self.svc_fake = svc_fake
        processed_highlight = "... "
        for key in highlight:
            if key == "doc.url":
                continue
            processed_highlight+=" ... ".join(highlight[key]) + " ... "
        self.highlight = processed_highlight

def search(request):
    if 'query' in request.GET:
        query = request.GET['query']
        page = int(request.GET['page']) if 'page' in request.GET else MIN_PAGE
        results = elastic_search(query, \
            results_number=PAGE_SIZE, \
            starting_position=(page - 1) * PAGE_SIZE)
        articles = [Article(**dict(results["hits"][i]['_source']["doc"].items() \
            + [("highlight", results["hits"][i]['highlight'])])) \
            for i in range(min(PAGE_SIZE, results["total"]))]
        
        # Pagination
        total_pages = int(math.ceil(1.0 * results["total"] / PAGE_SIZE))
        page = max(min(page, total_pages), MIN_PAGE)
        
        min_page_ = max(page - DELTA, MIN_PAGE)
        max_page_ = min(page + DELTA, total_pages)
        
        min_page = max(page - DELTA - (DELTA + page - max_page_) , MIN_PAGE)
        max_page = min(page + DELTA + abs(DELTA + min_page_ - page), total_pages)
        pages = range(min_page, max_page + 1)
        # End of Pagination

        return render(request, 'list.html', {'articles': articles, 'query': query, 'pages': pages, 'current_page': page, 'first_page': page == MIN_PAGE, 'last_page': page == total_pages })
    else:
        return render(request, 'list.html')