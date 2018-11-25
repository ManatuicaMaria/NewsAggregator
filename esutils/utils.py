from elasticsearch import Elasticsearch

INDEX_NAME = "news"
# BASE_URL = "http://localhost:9200/"
BASE_URL = "https://elastic:JRpwJMFmRdPFAC6Y5bJjGXSC@d1a97c5f7f1040619ec714d318846790.us-east-1.aws.found.io:9243"

es = Elasticsearch([BASE_URL], http_auth=('username', 'password'))