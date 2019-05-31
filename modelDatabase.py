import os
from datetime import date
from uuid import UUID, uuid4
from pony.orm import *
from emailSentiment import EmailSentiment

db_host = os.environ['DATABASE_HOST']
db_user = os.environ['DATABASE_USER']
db_pwd = os.environ['DATABASE_PWD']
db_name = os.environ['DATABASE_NAME']
database = Database()

class Email(database.Entity):
    sender = Required(str)
    subject = Required(str)
    received_date = Required(date)
    score = Optional(float)
    magnitude = Optional(float)
    sentences = Set('Sentence')
    PrimaryKey(sender, subject, received_date)

class Sentence(database.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required('Email')
    text = Required(str)
    sentiment = Required(float)
    position = Required(int)
    magnitude = Optional(float) 

class ModelDatabase:

    def __init__(self, *args, **kwargs):        
        return super().__init__(*args, **kwargs)

    def connect(self):
        database.bind(provider='postgres', host=db_host, database=db_name, user=db_user, password=db_pwd)
        database.generate_mapping(create_tables=True)

    @db_session
    def insert_email_data(self, email):
        inserted_email = Email(sender=email.sender, subject=email.subject, received_date=email.received, score=email.score, magnitude=email.magnitude)
        for index, sentence in enumerate(email.sentences):
            Sentence(email=inserted_email, text=sentence.text, sentiment=sentence.sentiment, magnitude=sentence.magnitude, position=index)
        return EmailSentiment(inserted_email)
    
    @db_session
    def retrieve_email_data(self, email):
        return EmailSentiment(Email[email.sender, email.subject, email.received])

    @db_session
    def update_sentence_sentiment(self, sentence_id, sentiment):
        sentence = Sentence[sentence_id]
        sentence.sentiment = sentiment
