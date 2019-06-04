import datetime

class EmailSentiment:

    def __init__(self, email_db = None):
        if email_db is not None:
            self._sender = email_db.sender
            self._subject = email_db.subject
            self._received = email_db.received_date
            self._score = email_db.score
            self._language = email_db.language
            self._magnitude = email_db.magnitude
            self._sentences = []
            sorted_sentences = sorted(email_db.sentences, key=lambda sentence: sentence.position)
            for sentence in sorted_sentences:
                self._sentences.append(Sentence(sentence.text, sentence.sentiment, sentence.magnitude, sentence.id))

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, value):
        self._sender = value

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = value

    @property
    def received(self):
        return self._received

    @received.setter
    def received(self, value):
        self._received = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    @property
    def magnitude(self):
        return self._magnitude

    @score.setter
    def magnitude(self, value):
        self._magnitude = value

    @property
    def sentences(self):
        return self._sentences

    @sentences.setter
    def sentences(self, value):
        self._sentences = value

    def sentences_from_google_nlp(self, google_sentences):
        self._sentences = []
        for sentence in google_sentences:
            self._sentences.append(Sentence(sentence.text.content, sentence.sentiment.score, sentence.sentiment.magnitude))


class Sentence():
    def __init__(self, text, sentiment, magnitude, id = None):
        self.text = text
        self.sentiment = sentiment
        self.magnitude = magnitude
        self.id = id