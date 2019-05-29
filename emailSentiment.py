import datetime

class EmailSentiment:

    def __init__(self):
        self._sender = ""
        self._subject = ""
        self._received = datetime.date(2019, 1, 1)
        self._score = 0
        self._magnitude = 0
        self._sentences = []

    def __init__(self, sender="", subject="", received=datetime.date(2019, 1, 1), score=0, magnitude=0, sentences=[]):
        self._sender = sender
        self._subject = subject
        self._received = received
        self._score = score
        self._magnitude = magnitude
        self._sentences = sentences

    def __init__(self, email_db = None):
        if email_db is not None:
            self._sender = email_db.sender
            self._subject = email_db.subject
            self._received = email_db.received_date
            self._score = email_db.score
            self._magnitude = email_db.magnitude
            self._sentences = []
            for sentence in email_db.sentences:
                self._sentences.append(Sentence(sentence.text, sentence.sentiment, sentence.magnitude))

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
        for sentence in google_sentences:
            self._sentences.append(Sentence(sentence.text.content, sentence.sentiment.score, sentence.sentiment.magnitude))


class Sentence():
    def __init__(self, text, sentiment, magnitude):
        self.text = text
        self.sentiment = sentiment
        self.magnitude = magnitude