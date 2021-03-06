import json
from elasticsearch.helpers import bulk
from news.fake_news_detection.predict import load_tokenizer, load_convolutional_network, predict_news
from news.fake_news_detection.PredictUtils import load_count_vectorizer, load_tf_idf_transfomer, \
    getWordCountProbabilities, getTfIdfProbabilities, load_passive_aggressive_clf, load_tfidf_linear_svc_clf
from utils import es, INDEX_NAME

# Payload for index configuration (set to default)
# {
#     "index" : {
#         "number_of_shards" : 5, 
#         "number_of_replicas" : 1
#     }
# }

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
            "_id": json_obj["url"]
        }


def index_bulk(json_array,
               index_name=INDEX_NAME):
    news_contents = [json_obj["content"] for json_obj in json_array]
    real_degrees = predict_news(convolutional_network, news_contents, tokenizer)
    pa_results = [getWordCountProbabilities(news_content, countVectorizer, passive_aggressive_clf) for news_content in
                  news_contents]
    svc_results = [getTfIdfProbabilities(news_content, countVectorizer, tfidfTransfomer, tfidf_linear_svc_clf) for
                   news_content in news_contents]
    for json_obj, real_degree, pa_result, svc_result in zip(*[json_array, real_degrees, pa_results, svc_results]):
        json_obj["real_degree"] = int(real_degree[0]*100)
        json_obj["pa_fake"] = pa_result
        json_obj["svc_fake"] = svc_result
    response = bulk(es, gendata(json_array, index_name), stats_only=True)
    success, failures = response
    print "Success: {}, Failures: {}".format(success, failures)


def index(json_obj,
          index_name=INDEX_NAME):
    news_content = [json_obj['content']]
    real_degree = predict_news(convolutional_network, news_content, tokenizer)
    pa_result = getWordCountProbabilities(news_content, countVectorizer, passive_aggressive_clf)
    svc_result = getTfIdfProbabilities(news_content, countVectorizer, tfidfTransfomer, tfidf_linear_svc_clf)
    json_obj["real_degree"] = int(real_degree[0][0] * 100)
    json_obj["pa_fake"] = pa_result
    json_obj["svc_fake"] = svc_result
    response = es.index(index=index_name, doc_type='_doc', body=json_obj, id=json_obj["url"])
    print response["result"]




# Examples of usages:

# Indexing
# print 'indexing article'
# article = Article("title", DUMMY_DESCRITION, URL, "24-11-2018", FAKE, REAL, 80)
# json_article = json.dumps(article.__dict__)
# index(json_obj=json_article)

# print 'indexing articles'
# json_article = {}
# json_article["title"] = "title"
# json_article["content"] = "bla"
# json_article["url"] = "URL"
# json_article["date"] = "24-11-2018"
# json_articles = [json_article, json_article]
# index_bulk(json_array=json_articles)

