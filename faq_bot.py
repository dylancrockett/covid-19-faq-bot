import re
from faq_updator import get_faq
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn


class FAQBot:
    def __init__(self, debug=False):
        # debug flag
        self.debug = debug

        # faq dict
        self.faq = get_faq()

        # faq questions array
        self.faq_questions = list(self.faq.keys())

    @staticmethod
    def convert_pen(tag):
        # Convert between a Penn Treebank tag to a simplified Wordnet tag
        if tag.startswith('N'):
            return 'n'

        if tag.startswith('V'):
            return 'v'

        if tag.startswith('J'):
            return 'a'

        if tag.startswith('R'):
            return 'r'

        return None

    def get_syn(self, word, tag):
        wn_tag = self.convert_pen(tag)
        if wn_tag is None:
            return None

        try:
            return wn.synsets(word, wn_tag)[0]
        except:
            return None

    def sentence_similarity(self, query_statement, question):
        # Tokenize and tag the query and question
        tokenized_query = pos_tag(word_tokenize(query_statement))
        tokenized_question = pos_tag(word_tokenize(question))

        # Get the synsets for the tagged words
        query_synsets = [self.get_syn(*tagged_word) for tagged_word in tokenized_query]
        question_synsets = [self.get_syn(*tagged_word) for tagged_word in tokenized_question]

        # Filter out None values
        query_synsets = [x for x in query_synsets if x is not None]
        question_synsets = [x for x in question_synsets if x is not None]

        # score and score count
        score = 0.0
        count = 0

        # for each word in the first sentence
        for synset in query_synsets:
            try:
                # get the similarity value of the most similar word in the other sentence
                best_score = max([synset.path_similarity(x) for x in question_synsets])

                # calculate score if possible
                if best_score is not None:
                    score += best_score
                    count += 1
            except:
                pass

        if count == 0:
            return 0

        # average the values
        score /= count
        return score

    # check which faq question matches the user question the best and give the appropriate response
    def get_faq_response(self, query):
        query_similarities = []

        # get the similarity between the query and each faq question
        for question in self.faq_questions:
            question = re.sub("[!?.,-]", '', question)

            query = re.sub("[!?.,-]", '', query)

            query_similarities.append(self.sentence_similarity(query, question))

        if self.debug:
            print("Query Similarity to FAQ Questions:")

            for x, question in enumerate(self.faq_questions):
                print("\t- " + question + ": " + str(query_similarities[x]))

        question = self.faq_questions[query_similarities.index(max(query_similarities))]

        return self.faq[question]
