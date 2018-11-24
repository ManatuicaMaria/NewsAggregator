import json
from elasticsearch import Elasticsearch

# Payload for index configuration (set to default)
# {
#     "index" : {
#         "number_of_shards" : 5, 
#         "number_of_replicas" : 1
#     }
# }

URL = "https://google.com"
DUMMY_DESCRITION="Lorem ipsum dolor sit amet, consectetur adipiscing elit. In luctus lobortis luctus. Duis eget lacus ultrices, aliquam arcu id, interdum quam. Praesent sollicitudin cursus blandit. Vestibulum ut libero semper, iaculis arcu et, vehicula felis. Pellentesque interdum ornare felis. Praesent at felis lacus. Etiam ac dapibus felis, sed faucibus lectus. Vestibulum ullamcorper eros eu diam ornare, auctor faucibus erat laoreet. Phasellus lobortis dolor at scelerisque pretium. Nulla facilisi. Nam et commodo dui. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nullam molestie sapien sed est auctor sollicitudin."
FAKE = "FAKE"
REAL = "REAL"
INDEX_NAME = "test"
ARTICLE_ID = "1"
BASE_URL = "http://localhost:9200/"
INDEX_UPDATE_ENDPOINT = "/_doc/"
SEARCH_URL = BASE_URL + "_search/"

es = Elasticsearch()

def index_update_url(index_name, article_id):
	return BASE_URL + index_name + INDEX_UPDATE_ENDPOINT + article_id + "?pretty"

class Article:

    def __init__(self, title, content, url, date, fake, real_degree):
        self.title = title
        self.content = content
        self.url = url
        self.date = date
        self.fake = fake == FAKE
        self.real_degree = real_degree

# Indexing
print 'indexing article'
article = Article("title", DUMMY_DESCRITION, URL, "24-11-2018", FAKE, 80)
json_article = json.dumps(article.__dict__)
response = es.index(index=INDEX_NAME, doc_type='_doc', body=json_article)
print response["result"]

# Searching
print 'searching'
match = {}
match["content"] = "libero semper" #query for article that contains either libero or semper in content
query = {}
query["match"] = match
payload = {}
payload["query"] = query
payload["size"] = 10 #number of results to return (for pagination)
payload["from"] = 0 #starting position (for pagination)
json_payload = json.dumps(payload)
response = es.search(index="_all", body=json_payload)
print("Got %d Hits:" % response['hits']['total'])
for hit in response['hits']['hits']:
    print(hit["_source"])
