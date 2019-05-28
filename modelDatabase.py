import os
from datetime import date
from uuid import UUID, uuid4
from pony.orm import *

db_host = os.environ['DATABASE_HOST']
db_user = os.environ['DATABASE_USER']
db_pwd = os.environ['DATABASE_PWD']
db_name = os.environ['DATABASE_NAME']

class ModelDatabase:
    def __init__(self, *args, **kwargs):
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
            id = PrimaryKey(UUID, auto=True)
            email = Required(Email)
            text = Required(str)
            sentiment = Required(float)
            magnitude = Optional(float) 
        self.db = database
        return super().__init__(*args, **kwargs)

    def connect(self):
        self.db.bind(provider='postgres', host=db_host, database=db_name, user=db_user, password=db_pwd)
        self.db.generate_mapping(create_tables=True)


    @db_session
    def insert_email_data(self, email):
        inserted_email = Email(sender=email.sender, subject=email.subject, received_date=email.received, score=email.score, magnitude=email.magnitude)
        for sentence in email.sentences:
            Sentence(email=inserted_email, text=sentence.text.content, sentiment=sentence.sentiment.score, magnitude=sentence.sentiment.magnitude)
