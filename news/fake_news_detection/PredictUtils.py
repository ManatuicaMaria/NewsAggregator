# -*- coding: utf-8 -*-

import time, json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.externals import joblib

import os

dir_path = os.path.dirname(os.path.realpath(__file__))

COUNT_VECTORIZER = dir_path + "/trained_models/count_vectorizer.pkl"
TFIDF_TRANSFORMER = dir_path + "/trained_models/tfidf_transformer.pkl"
TFIDF_LINEAR_SVC = dir_path + "/trained_models/Tfidf_LinearSVC.pkl"
WC_PASSIVE_AGRESSIVE = dir_path + "/trained_models/WC_PassiveAggressiveClassifier.pkl"


def saveClassificationData():
    countVectorizer = CountVectorizer(encoding='utf-8', decode_error='strict', strip_accents=None, lowercase=True,
                                      preprocessor=None, tokenizer=None, stop_words='english', ngram_range=(1, 1),
                                      analyzer='word', max_features=None, vocabulary=None, binary=False)

    tfidfTransformer = TfidfTransformer(norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False)

    print 'loading the data...'
    news = []
    start = time.time()
    with open('data.json') as news_file:
        newsJSON = json.load(news_file)
        for pieceOfNews in newsJSON:
            news.append(pieceOfNews['content'])
    end = time.time()
    print str(end - start) + ' seconds to load the data'

    print 'computing word count'
    start = time.time()
    features = countVectorizer.fit_transform(news)
    joblib.dump(countVectorizer, COUNT_VECTORIZER)
    end = time.time()
    print 'done word count'

    print 'computing tfidf'
    start = time.time()
    tfidfTransformer.fit_transform(features)
    joblib.dump(tfidfTransformer, TFIDF_TRANSFORMER)
    end = time.time()
    print 'done tfidf'

    print 'done loading data'


def load_count_vectorizer():
    return joblib.load(COUNT_VECTORIZER)


def load_tf_idf_transfomer():
    return joblib.load(TFIDF_TRANSFORMER)


def load_tfidf_linear_svc_clf():
    return joblib.load(TFIDF_LINEAR_SVC)


def load_passive_aggressive_clf():
    return joblib.load(WC_PASSIVE_AGRESSIVE)


def getTfIdfProbabilities(text, countVectorizer, tfidfTransformer, clf):
    features = countVectorizer.transform([text])
    tfidfFeatures = tfidfTransformer.transform(features)

    # returns list of probabilities, in order of classes
    # I think first is real, second is fake
    # training label value: 1 - fake, 0 - real
    label = clf.predict(tfidfFeatures)[0]
    return label


def getWordCountProbabilities(text, countVectorizer, clf):

    wcFeatures = countVectorizer.transform([text])

    # returns list of probabilities, in order of classes
    # I think first is real, second is fake
    # training label value: 1 - fake, 0 - real
    label = clf.predict(wcFeatures)[0]
    return label


def getWord2VecProbabilities(text):
    pass


def getGloveProbabilities(text):
    pass


if __name__ == '__main__':
    text = "After Vets Fight War, Feds Demand Money Back U.S. government continues to treat troops like second class citizens Infowars Nightly News - October 27, 2016 Comments Thanks you for your service? No. After promising bonuses & education benefits to military in order to get them to re-enlist for the Afghanistan & Iraq Wars, the Pentagon is now demanding the money back from vets who can’t afford to pay. This is how Obama treats veterans — just like Hillary treats those who protect her in the Secret Service. Can anyone trust their promises? NEWSLETTER SIGN UP Get the latest breaking news & specials from Alex Jones and the Infowars Crew. Related Articles"
    countVectorizer = load_count_vectorizer()
    tfidfTransfomer = load_tf_idf_transfomer()
    tfidf_linear_svc_clf = load_tfidf_linear_svc_clf()
    passive_aggressive_clf = load_passive_aggressive_clf()
    print "Done loading"
    print str(getWordCountProbabilities(text, countVectorizer, passive_aggressive_clf))
    print str(getTfIdfProbabilities(text, countVectorizer, tfidfTransfomer, tfidf_linear_svc_clf))
