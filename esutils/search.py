from utils import es, INDEX_NAME

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
        query_fields = ["doc.content", "doc.title", "doc.author", "doc.date", "doc.url"]
    if highlight_fields is None:
        highlight_fields = {"doc.content": {},
                            "doc.title": {},
                            "doc.author": {},
                            "doc.date": {},
                            "doc.url": {}}
    should = []
    for field in query_fields:
        match = {field: query_content}
        should.append({"match": match})
    boolean = {"should": should}
    query = {"bool": boolean}
    payload = {"query": query, "size": results_number, "from": starting_position}
    highlight = {"fields": highlight_fields}
    payload["highlight"] = highlight
    response = es.search(index=INDEX_NAME, body=payload)
    return response['hits']

def main():
    # Searching
    print('searching')
    response = search(query_content="for")
    print("Got %d Hits:" % response['total'])
    for hit in response['hits']:
        print(hit["_source"])
        print(hit["highlight"])

if __name__ == "__main__":
    main()


