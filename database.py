import os
import datetime
import psycopg2

db_host = os.environ['DATABASE_HOST']
db_user = os.environ['DATABASE_USER']
db_pwd = os.environ['DATABASE_PWD']
db_name = os.environ['DATABASE_NAME']

class Database:

    def __init__(self, receiver="", sender="", subject="", received=datetime.date(2019, 1, 1), score=0, magnitude=0, sentences=[]):
        self._receiver = receiver
        self._sender = sender
        self._subject = subject
        self._received = received
        self._score = score
        self._magnitude = magnitude
        self._sentences = sentences

    @property
    def receiver(self):
        return self._receiver

    @receiver.setter
    def receiver(self, value):
        self._receiver = value

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
    

    def connect(self):
        self.conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pwd)


    def close(self):
        self.conn.close()


    def insert_email_data(self):
        cur = self.conn.cursor()
        insert_sentences_value = """ARRAY ["""
        for sentence in self._sentences:
            insert_sentences_value += """ROW(%s, %s, %s),""",(sentence.text.content, sentence.sentiment.score, sentence.sentiment.magnitude)
        insert_sentences_value = insert_sentences_value[:-1]
        insert_sentences_value += """]"""
        cur.execute(
            """
            INSERT INTO Emails (receiver, sender, subject, received, score, magnitude, sentences)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """,
            (self._receiver, self._sender, self._subject, self._received, self._score, self._score, self._magnitude, insert_sentences_value)
        )
        cur.close()
        self.conn.commit()


    def create_sentence_type(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TYPE Sentence AS (
                text VARCHAR(2500),
                sentiment FLOAT(2),
                magnitude FLOAT(2)
            )
            """
        )
        cur.close()
        self.conn.commit()


    def create_email_table(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE Emails (
                email_id SERIAL,
                receiver VARCHAR(255),
                sender VARCHAR(255),
                subject VARCHAR(255),
                received DATE,
                score FLOAT(2),
                magnitude FLOAT(2),
                sentences Sentence[],
                PRIMARY KEY (receiver, sender, subject, received)
            )
            """
        )
        cur.close()
        self.conn.commit()