import mysql.connector
from flask import Flask, render_template, request
import my_graph as gp

conn = mysql.connector.connect(host='127.0.0.1', user='tweetuser', password='tweetpasswd', database='tweets')
myCur = conn.cursor()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("search.html")


@app.route('/searchdata', methods=['POST'])
def search_tweets():
    search = request.form['search']
    myCur.execute("SELECT my_date, tweet, sentiment, confidence FROM tweets")
    data = myCur.fetchall()

    my_list = []
    total = 0
    pos = 0
    neg = 0
    neu = 0
    message = ""
    tweets = open("graph_data.txt","w")
    for row in data:
        if search in row[1]:
            tweets.write(row[2])
            tweets.write('\n')
            dt = row[0]
            dtstr = dt.strftime("%d, %B, %Y")
            the_row = [dtstr]
            the_row.append(row[1:])
            my_list.append(the_row)

        if search in row[1] and row[2] == "positive":
            total += 1
            pos += 1
        elif search in row[1] and row[2] == "negative":
            total += 1
            neg += 1
        elif search in row[1] and row[2] == "neutral":
            total += 1
            neu += 1

    if pos > neg and pos > neu: # overall evaluation based on the highes count of either positive, negative or neutral tweets
        message = "Positive, as " + str(pos) + " tweet(s) were positive, " + str(neg) + " tweet(s) were negative, " + str(neu) + \
                  " tweet(s) were neutral out of the total of " + str(total)
    elif neg > pos and neg > neu:
        message = "Negative, as " + str(neg) + " tweet(s) were negative, " + str(pos) + " tweet(s) were positive, " + str(neu) + \
                  " tweet(s) were neutral out of the total of " + str(total)
    elif neu > pos and neu > neg:
        message = "Neutral, as " + str(neu) + " tweet(s) were neutral, " + str(pos) + " tweet(s) were positive, " + str(neg) + \
                  " tweet(s) were negative out of the total of " + str(total)
    else:
        message = "No overall evaluation, as no one category of tweets was greater than the rest, or no tweets were found..."

    return render_template("results.html",
                            search = search,
                            total_evaluation = message,
                            results = my_list,
                            graph = gp,)


if __name__ == '__main__':
    app.run(debug=True)