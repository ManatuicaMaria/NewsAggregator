from utils import es

'''
    Am mutat aici functia deoarece altfel se incarcau modele
    inutil la rularea serverului
'''

def search(query_content,
           results_number=10,
           starting_position=0,
           query_fields=None,
           highlight_fields=None):
    if query_fields is None:
        query_fields = ["content", "title", "author", "date", "url"]
    if highlight_fields is None:
        highlight_fields = {"content": {},
                            "title": {},
                            "author": {},
                            "date": {},
                            "url": {}}
    should = []
    for field in query_fields:
        match = {field: query_content}
        should.append({"match": match})
    boolean = {"should": should}
    query = {"bool": boolean}
    payload = {"query": query, "size": results_number, "from": starting_position}
    highlight = {"fields": highlight_fields}
    payload["highlight"] = highlight
    response = es.search(index="_all", body=payload)
    return response['hits']