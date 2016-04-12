import nltk
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC
from nltk.classify import ClassifierI
import pickle
import positive, negative, neutral

from statistics import mode


class Vote(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers: #c for classifiers
            v = c.classify(features) #v for votes
            votes.append(v)
        #print(votes)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers: #c for classifiers
            v = c.classify(features) #v for votes
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

classifier = nltk.NaiveBayesClassifier.train(training_set)

# print("original_classifier accuracy percentage:", (nltk.classify.accuracy(classifier, testing_set))*100)
# #
# #pickle classifier
save_original_classifier = open("pickled_algorithms/original.pickle","wb")
pickle.dump(classifier, save_original_classifier)
save_original_classifier.close()
print("done")
#
MultinomialNB_classifier = SklearnClassifier(MultinomialNB())
MultinomialNB_classifier.train(training_set)

#print("MultinomialNB_classifier accuracy percentage:", (nltk.classify.accuracy(MultinomialNB_classifier, testing_set))*100)
# #
# # #pickle classifier
save_MultinomialNB_classifier = open("pickled_algorithms/MultinomialNB.pickle","wb")
pickle.dump(MultinomialNB_classifier, save_MultinomialNB_classifier)
save_MultinomialNB_classifier.close()
print("done")
#
BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
# print("done")
# print("BernoulliNB_classifier accuracy percentage:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
#
# #pickle classifier
save_BernoulliNB_classifier = open("pickled_algorithms/BernoulliNB.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_BernoulliNB_classifier)
save_BernoulliNB_classifier.close()
print("done")
#
LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)

# print("LogisticRegression_classifier accuracy percentage:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
#
# #pickle classifier
save_LogisticRegression_classifier = open("pickled_algorithms/LogisticRegression.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_LogisticRegression_classifier)
save_LogisticRegression_classifier.close()
print("done")
#
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)

# print("LinearSVC_classifier accuracy percentage:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
#
# #pickle classifier
save_LinearSVC_classifier = open("pickled_algorithms/LinearSVC.pickle","wb")
pickle.dump(LinearSVC_classifier, save_LinearSVC_classifier)
save_LinearSVC_classifier.close()
print("done")
#
SGD_classifier = SklearnClassifier(SGDClassifier())
SGD_classifier.train(training_set)

# print("SGD_classifier accuracy percentage:", (nltk.classify.accuracy(SGD_classifier, testing_set))*100)
#
# #pickle classifier
save_SGD_classifier = open("pickled_algorithms/SGDClassifier.pickle","wb")
pickle.dump(SGD_classifier, save_SGD_classifier)
save_SGD_classifier.close()
print("done")
#
# # #---------low accuracy---------------
SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)

# print("SVC_classifier accuracy percentage:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)
#
# #pickle classifier
save_SVC_classifier = open("pickled_algorithms/SVC.pickle","wb")
pickle.dump(SVC_classifier, save_SVC_classifier)
save_SVC_classifier.close()
print("done")

# #------------------combined all classifiers------------------
# voted_classifiers = Vote(classifier,
#                         MultinomialNB_classifier,
#                         BernoulliNB_classifier,
#                         LogisticRegression_classifier,
#                         LinearSVC_classifier,
#                         SGD_classifier,
#                         SVC_classifier)
#
# # print("voted_classifier accuracy percentage:", (nltk.classify.accuracy(voted_classifiers, testing_set))*100)
#
# def sentiment(text):
#     features = extract_features(text.split())
#     return voted_classifiers.classify(features),voted_classifiers.confidence(features)
