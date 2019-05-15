import os
import datetime
import psycopg2

db_host = os.environ['DATABASE_HOST']
db_user = os.environ['DATABASE_USER']
db_pwd = os.environ['DATABASE_PWD']
db_name = os.environ['DATABASE_NAME']

class Database:

    def connect(self):
        self.conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pwd)


    def close(self):
        self.conn.close()


    def insert_email_data(self, email):
        cur = self.conn.cursor()
        insert_sentences_value = []
        for sentence in email.sentences:
            insert_sentences_value.append((sentence.text.content, sentence.sentiment.score, sentence.sentiment.magnitude))
        cur.execute(
            """
            INSERT INTO Emails (sender, subject, received, score, magnitude, sentences)
            VALUES(%s, %s, %s, %s, %s, %s::Sentence[])
            """
            ,(email.sender, email.subject, email.received, email.score, email.magnitude, insert_sentences_value)
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
                sender VARCHAR(255),
                subject VARCHAR(255),
                received DATE,
                score FLOAT(2),
                magnitude FLOAT(2),
                sentences Sentence[],
                PRIMARY KEY (sender, subject, received)
            )
            """
        )
        cur.close()
        self.conn.commit()