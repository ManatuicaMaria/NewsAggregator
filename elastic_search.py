import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from news.fake_news_detection.predict import load_tokenizer, load_convolutional_network, predict_news
from news.fake_news_detection.PredictUtils import load_count_vectorizer, load_tf_idf_transfomer, getWordCountProbabilities, getTfIdfProbabilities, load_passive_aggressive_clf, load_tfidf_linear_svc_clf

# Payload for index configuration (set to default)
# {
#     "index" : {
#         "number_of_shards" : 5, 
#         "number_of_replicas" : 1
#     }
# }

INDEX_NAME = "news"
# BASE_URL = "http://localhost:9200/"
BASE_URL = "https://elastic:JRpwJMFmRdPFAC6Y5bJjGXSC@d1a97c5f7f1040619ec714d318846790.us-east-1.aws.found.io:9243"

es=Elasticsearch([BASE_URL], http_auth=('username', 'password'))

tokenizer = load_tokenizer()
convolutional_network = load_convolutional_network(tokenizer)

countVectorizer = load_count_vectorizer()
tfidfTransfomer = load_tf_idf_transfomer()
tfidf_linear_svc_clf = load_tfidf_linear_svc_clf()
passive_aggressive_clf = load_passive_aggressive_clf()

def gendata(json_array, index_name=INDEX_NAME):
	for json_obj in json_array:
		yield {
            "_index": index_name,
            "_type": "_doc",
            "doc": json_obj,
        }

def index_bulk(	json_array, 
	index_name=INDEX_NAME):
	news_contents = [json_obj["content"] for json_obj in json_array]
	real_degrees = predict_news(convolutional_network, news_contents, tokenizer)
	pa_results = [getWordCountProbabilities(news_content, countVectorizer, passive_aggressive_clf) for news_content in news_contents]
	svc_results = [getTfIdfProbabilities(news_content, countVectorizer, tfidfTransfomer, tfidf_linear_svc_clf) for news_content in news_contents]
	for json_obj, real_degree, pa_result, svc_result in zip(*[json_array, real_degrees, pa_results, svc_results]):
		json_obj["real_degree"] = real_degree[1]
		json_obj["pa_fake"] = pa_result
		json_obj["svc_fake"] = svc_result
	response = bulk(es, gendata(json_array, index_name), stats_only=True)
	success, failures = response
	print "Success: {}, Failures: {}".format(success, failures)

def index(json_obj, 
	index_name=INDEX_NAME):
	response = es.index(index=INDEX_NAME, doc_type='_doc', body=json_obj)
	print response["result"]

def search(query_content,
	results_number=10,
	starting_position=0,
	query_fields=["content", "title", "author", "date", "url"],
	highlight_fields={"content": {},
					  "title": {},
					  "author": {},
					  "date": {},
					  "url": {}}):
	should = []
	for field in query_fields:
		match = {}
		match[field] = query_content #query for article that contains either one of the words in content
		should.append({"match": match})
	boolean = {}
	boolean["should"] = should
	query = {}
	query["bool"] = boolean
	payload = {}
	payload["query"] = query
	payload["size"] = results_number #number of results to return (for pagination)
	payload["from"] = starting_position #starting position (for pagination)
	highlight = {}
	highlight["fields"] = highlight_fields
	payload["highlight"] = highlight
	response = es.search(index="_all", body=payload)
	return response['hits']

#Examples of usages:

# Indexing
# print 'indexing article'
# article = Article("title", DUMMY_DESCRITION, URL, "24-11-2018", FAKE, REAL, 80)
# json_article = json.dumps(article.__dict__)
# index(json_obj=json_article)

# print 'indexing articles'
# json_article = {}
# json_article["title"] = "title"
# json_article["content"] = DUMMY_DESCRITION
# json_article["url"] = URL
# json_article["date"] = "24-11-2018"
# json_articles = [json_article, json_article]
# index_bulk(json_array=json_articles)

# Searching
# print 'searching'
# response = search(query_content="24")
# print("Got %d Hits:" % response['total'])
# for hit in response['hits']:
#     print(hit["_source"])
#     print(hit["highlight"])
