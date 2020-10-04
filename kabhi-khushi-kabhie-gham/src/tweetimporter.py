from flask import Flask, jsonify, request
from twitter import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sys
import json

app = Flask(__name__)

@app.route('/tweetSentiments')
def twitterSentimentData():
    analyzer = SentimentIntensityAnalyzer()

    model_id = 'cl_pi3C7JiL'

    #-----------------------------------------------------------------------
    # create twitter API object
    #-----------------------------------------------------------------------

    api_key = "8DyszqLCLYaROTiNeusRlDI6C"
    api_key_secret = "mTNbMxyEVyiH27JGcPZaTAv1Ufo01lDiAx9fZlYntdbm0xchI5"

    access_token = "2899810486-Y3oB2YIIQcsJtRg8M7Kqly8TZn8IyOh738PsdOm"
    access_token_secret = "wRbOffiMGsMWoD9JoBWKrQp82nD52MyWbWlZhGVFAgVvD"
    twitter = Twitter(auth = OAuth(access_token, access_token_secret, api_key, api_key_secret))


    monthMapping = dict()
    monthMapping["Jan"] = "01"
    monthMapping["Feb"] = "02"
    monthMapping["Mar"] = "03"
    monthMapping["Apr"] = "04"
    monthMapping["May"] = "05"
    monthMapping["Jun"] = "06"
    monthMapping["Jul"] = "07"
    monthMapping["Aug"] = "08"
    monthMapping["Sep"] = "09"
    monthMapping["Oct"] = "10"
    monthMapping["Nov"] = "11"
    monthMapping["Dec"] = "12"
    
    def getSentimentData(user):
        

        d = dict()
        texts = list()
        first = True

        results = list()
        lastId = None
        while True:
            #print ("here")
            if first:
                first = False
                results = twitter.statuses.user_timeline(screen_name = user, count = 200, exclude_replies=True, include_rts=False)
                #print (results)
                #print (len(results))
                if len(results) == 1:
                    break

            else:
                newResults = twitter.statuses.user_timeline(screen_name = user, count = 200, exclude_replies=True, include_rts=False, max_id = lastId)
                #print (len(newResults))
                if len(newResults) == 1:
                    break
                results.extend(newResults)

            lastId = results[len(results) - 1]["id"]

        dates = list()
        for status in results:
            date = status["created_at"]
            splitted = date.split(" ")
            finalDateUSFormat = monthMapping[splitted[1]] + "/" + splitted[2] + "/" + splitted[5]
            text = str(status["text"].encode("ascii", "ignore"))[2:]
            scores = analyzer.polarity_scores(text)

            if scores["compound"] > 0.1:
                sentiment = "positive"
            elif scores["compound"] < -0.1:
                sentiment = "negative"
            else:
                sentiment = "none"
            #print (text)
            #print (sentiment)
            #print ("------------")
            if sentiment == "positive":
                if finalDateUSFormat in d:
                    cur = d[finalDateUSFormat]
                    d[finalDateUSFormat] = (cur[0] + 1, cur[1])
                else:
                    d[finalDateUSFormat] = (1, 0)

            elif sentiment == "negative":
                if finalDateUSFormat in d:
                    cur = d[finalDateUSFormat]
                    d[finalDateUSFormat] = (cur[0], cur[1] + 1)
                else:
                    d[finalDateUSFormat] = (0, 1)            
        
        return jsonify(d)

    args = request.args
    #print(args)
    userID = args['id']
    #print(userID)
    return getSentimentData(userID)


if __name__ == '__main__':
    app.run()


