import json
import re
import time
from threading import Thread
import requests
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from general import util
from models.constants import ServerEnum
import pickle
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import wordnet
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from gensim.test.utils import common_texts
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


@csrf_exempt
def getHotelDashboard(request):
    try:
        requestBody = util.decodeJson(request.body)

        page = requestBody['page']


        hotelDatabaseResult = util.executesql(
            query="SELECT * FROM hotels_table",
            datatuple=[])
            
        hotels = []
        iter = 5
        iter += page

        for hotel in hotelDatabaseResult:
            if iter == 0:
                break
            # print(hotel[3])
            hotelDetails = util.getObjectFromBinaryDecode(hotel[3])
            data = {"id": hotel[0], "name": hotel[1], "isRecommended": hotel[2], 
                        'hotelAddress': hotelDetails['hotelAddress'], 
                        'description': hotelDetails['description'],
                        'amenities': hotelDetails['amenities']}
            hotels.append(data)

            iter -= 1

            # print(data)



        return JsonResponse({
            'hotelData': hotels,
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN getHotelDashboard() method in recommender/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()


@csrf_exempt
def getHotelOnCountry(request):
    try:
        requestBody = util.decodeJson(request.body)

        country = requestBody['country']

        hotelDatabaseResult = util.executesql(
            query="SELECT * FROM hotels_table WHERE country = %s",
            datatuple=[country])

        return JsonResponse({
            'hotelData': hotelDatabaseResult,
            'status': True,
            'responseMessage': ServerEnum.ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN getHotelOnCountry() method in recommender/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()


@csrf_exempt
def getHotelOnName(request):
    try:
        requestBody = util.decodeJson(request.body)

        hotelName = requestBody['hotelName']

        hotelDatabaseResult = util.executesql(
            query="SELECT * FROM hotels_table WHERE hotelName = %s",
            datatuple=[hotelName])

        return JsonResponse({
            'hotelData': hotelDatabaseResult,
            'status': True,
            'responseMessage': ServerEnum.ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN getHotelOnName() method in recommender/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()


@csrf_exempt
def getHotelReviews(request):
    try:
        requestBody = util.decodeJson(request.body)

        hotelId = requestBody['hotelId']

        reviewResult = util.executesql(
            query="SELECT * FROM reviews_table WHERE hotelId = %s",
            datatuple=[hotelId])

        return JsonResponse({
            'reviews': reviewResult,
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN getHotelReviews() method in recommender/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()


@csrf_exempt
def setHotelReview(request):
    try:
        # nltk.download('stopwords')
        # nltk.download('vader_lexicon')
        # put into reviews_table, put sentiment, update hotel's recommendation status
        requestBody = util.decodeJson(request.body)

        hotelId = requestBody['hotelId']
        reviewBody = requestBody['reviewBody']
        email = requestBody['email']

        name = util.executesql(query="SELECT firstName, secondName from customer_user_table where userEmail = %s",
                                datatuple=[email])

        name = name[0][0] + ' ' + name[0][1]

        reviewId = util.generateID("REVIEW")

        sentiment = getReviewSentiment(reviewBody)

        total_neg_reviews = util.executesql(query="SELECT SUM(sentiment) FROM reviews_table WHERE hotelId = %s",
                                            datatuple=[hotelId])[0][0]

        all_reviews = util.executesql(query="SELECT COUNT(reviewId) FROM reviews_table WHERE hotelId = %s",
                                       datatuple=[hotelId])[0][0]

        # print(total_neg_reviews, all_reviews)

        percentage = total_neg_reviews / all_reviews

        recommend = 1

        if percentage > 0.6:
            recommend = 0

        util.executesql(query="UPDATE hotels_table SET isRecommended = %s WHERE hotelId = %s",
                            datatuple=[recommend, hotelId])

        util.executesql(query="INSERT INTO reviews_table (reviewId, hotelId, reviewBody, sentiment, reviewerName) VALUES \
                                (%s, %s, %s, %s, %s)",
                            datatuple=[reviewId, hotelId, reviewBody, recommend, name])

        return JsonResponse({
            'name': name,
            'status': True,
            'responseMessage': ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN setHotelReview() method in recommender/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()


@csrf_exempt
def singleHotelDetails(request):
    try:

        requestBody = util.decodeJson(request.body)

        hotelId = requestBody['hotelId']

        hotelData = util.executesql(query="SELECT * FROM hotels_table WHERE hotelId = %s",
                                            datatuple=[hotelId[0]])[0][0]

        hotelDetails = util.getObjectFromBinaryDecode(hotelData[3])
        data = {"id": hotelData[0], "name": hotelData[1], "isRecommended": hotelData[2], 
                        'hotelAddress': hotelDetails['hotelAddress'], 
                        'description': hotelDetails['description'],
                        'amenities': hotelDetails['amenities']}

        return JsonResponse({
            'hotelData' : data,
            'status': True,
            'responseMessage': ServerEnum.ServerEnum.RESPONSE_SUCCESS
        })

    except Exception as e:
        print("ERROR IN setHotelReview() method in recommender/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()


def getReviewSentiment(review):
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
    model = pickle.load(open('doc2vec.sav', 'rb'))
    features = pickle.load(open("feature.sav", 'rb'))

    # tmp_df = pd.DataFrame(data=np.zeros((1,len(features))), columns=features)

    tree_features = 3837
    
    data = {'review': [review], 'review_clean': [clean_text(review)]}

    reviews_df = pd.DataFrame(data=data)
    # reviews_df['review'] = review
    # reviews_df['review_clean'] = clean_text(review)

    sid = SentimentIntensityAnalyzer()
    reviews_df["sentiments"] = reviews_df["review"].apply(
        lambda x: sid.polarity_scores(x))
    reviews_df = pd.concat([reviews_df.drop(
        ['sentiments'], axis=1), reviews_df['sentiments'].apply(pd.Series)], axis=1)

    reviews_df["nb_chars"] = float(reviews_df["review"].apply(lambda x: len(x)))
    reviews_df["nb_words"] = float(reviews_df["review"].apply(
        lambda x: len(x.split(" "))))

    documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(
        reviews_df["review_clean"].apply(lambda x: x.split(" ")))]

    # model = Doc2Vec(documents, vector_size=5, window=2, min_count=5, workers=4)
    
    doc2vec_df = reviews_df["review_clean"].apply(
        lambda x: model.infer_vector(x.split(" "))).apply(pd.Series)

    doc2vec_df.columns = ["doc2vec_vector_" +
                          str(x) for x in doc2vec_df.columns]
    reviews_df = pd.concat([reviews_df, doc2vec_df], axis=1)

    tfidf = TfidfVectorizer(min_df=1)
    tfidf_result = tfidf.fit_transform(reviews_df["review_clean"]).toarray()
    tfidf_df = pd.DataFrame(tfidf_result, columns=tfidf.get_feature_names())
    tfidf_df.columns = ["word_" + str(x) for x in tfidf_df.columns]
    tfidf_df.index = reviews_df.index
    reviews_df = pd.concat([reviews_df, tfidf_df], axis=1)

    col_num = len(reviews_df.columns)

    if col_num < tree_features:
        ones = np.ones((1, tree_features - col_num+2), dtype='float')
        dummy_cols = ["dummy_"+str(i) for i in range(tree_features - col_num+2)]
        ones = pd.DataFrame(data=ones, columns=dummy_cols)

        reviews_df = pd.concat([reviews_df, ones], axis=1)

    ignore_cols = ["review", "review_clean"]
    features = [c for c in reviews_df.columns if c not in ignore_cols]

    return loaded_model.predict(reviews_df[features].values)


def clean_text(text):

    text = text.lower()
    text = [word.strip(string.punctuation) for word in text.split(" ")]
    # remove words that contain numbers
    text = [word for word in text if not any(c.isdigit() for c in word)]
    # remove stop words
    stop = stopwords.words('english')
    text = [x for x in text if x not in stop]
    # remove empty tokens
    text = [t for t in text if len(t) > 0]
    # pos tag text
    pos_tags = pos_tag(text)
    # lemmatize text
    porter = PorterStemmer()
    text = [WordNetLemmatizer().lemmatize(t[0], get_wordnet_pos(t[1]))
            for t in pos_tags]
    # remove words with only one letter
    text = [t for t in text if len(t) > 1]
    # join all
    text = " ".join(text)
    return(text)


def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


# ------------------------------------------------------------------------------------- #

@csrf_exempt
def setHotelRecommends(request):
    try:
        hotelIds = util.executesql(
            query="SELECT hotelId FROM hotels_table",
            datatuple=[])

        for hotelId in hotelIds:
            total_neg_reviews = util.executesql(query="SELECT SUM(sentiment) FROM reviews_table WHERE hotelId = %s",
                                            datatuple=[hotelId[0]])[0][0]

            all_reviews = util.executesql(query="SELECT COUNT(reviewId) FROM reviews_table WHERE hotelId = %s",
                                            datatuple=[hotelId[0]])[0][0]


            percentage = total_neg_reviews / all_reviews

            recommend = 1

            if percentage > 0.6:
                recommend = 0

            util.executesql(query="UPDATE hotels_table SET isRecommended = %s WHERE hotelId = %s",
                                            datatuple=[recommend, hotelId[0]])
            
        return JsonResponse({
                'status': True,
                'responseMessage': ServerEnum.RESPONSE_SUCCESS
            })

    except Exception as e:
        print("ERROR IN setHotelRecommends() method in database/views.py")
        print(e)
        return util.sendDatabaseConnectionErrorResponse()