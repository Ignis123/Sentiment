import nltk
from nltk.classify import ClassifierI
from statistics import mode
import pickle
import positive, negative, neutral


class Vote(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        print(votes)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

tweets = []
for (words, sentiment) in positive.tweets + negative.tweets + neutral.tweets:
    filtered_words = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((filtered_words, sentiment))


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


word_features = get_word_features(get_words_in_tweets(tweets))


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


training_set = nltk.classify.apply_features(extract_features, tweets)


# open pickled file
open_file = open("pickled_algorithms/original.pickle", "rb")
original_classifier = pickle.load(open_file)
open_file.close()
#print("Original_classifier accuracy percentage:", (nltk.classify.accuracy(original_classifier, testing_set))*100) <-- to test if pickled classifiers work

#open pickled file
open_file = open("pickled_algorithms/MultinomialNB.pickle", "rb")
MNB_classifier = pickle.load(open_file)
open_file.close()
#print("MNB_classifier accuracy percentage:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

#open pickled file
open_file = open("pickled_algorithms/BernoulliNB.pickle", "rb")
BernoulliNB_classifier = pickle.load(open_file)
open_file.close()
#print("BernoulliNB_classifier accuracy percentage:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

#open pickled file
open_file = open("pickled_algorithms/LogisticRegression.pickle", "rb")
LogisticRegression_classifier = pickle.load(open_file)
open_file.close()
#print("LogisticRegression_classifier accuracy percentage:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

#open pickled file
open_file = open("pickled_algorithms/LinearSVC.pickle", "rb")
LinearSVC_classifier = pickle.load(open_file)
open_file.close()
#print("LinearSVC_classifier accuracy percentage:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

#open pickled file
open_file = open("pickled_algorithms/SGDClassifier.pickle", "rb")
SGD_classifier = pickle.load(open_file)
open_file.close()
#print("SGD_classifier accuracy percentage:", (nltk.classify.accuracy(SGD_classifier, testing_set))*100)

#open pickled file
open_file = open("pickled_algorithms/SVC.pickle", "rb")
SVC_classifier = pickle.load(open_file)
open_file.close()
#print("SVC_classifier accuracy percentage:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

#run all classifiers togother to decide if positive or negative
voted_classifiers = Vote(original_classifier,
                         LinearSVC_classifier,
                         MNB_classifier,
                         BernoulliNB_classifier,
                         LogisticRegression_classifier,
                         SGD_classifier,
                         SVC_classifier)

#print("voted_classifier accuracy percentage:", (nltk.classify.accuracy(voted_classifiers, testing_set))*100) <-- to test if combined classification works


def sentiment(text):
    features = extract_features(text.split())
    return voted_classifiers.classify(features),voted_classifiers.confidence(features)*100
