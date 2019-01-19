from elasticsearch import Elasticsearch

INDEX_NAME = "news"
# BASE_URL = "http://localhost:9200/"
BASE_URL = "https://elastic:CkKEyz8ZyNvhjhUwtDhPnzj3@56a6a02d817f427d94311d32afd28239.us-east-1.aws.found.io:9243"

es = Elasticsearch([BASE_URL], http_auth=('username', 'password'))