import pandas as pd
import numpy as np
import string
from stop_words import get_stop_words
import joblib
from stop_words import get_stop_words
import tensorflow as tf
from mysql.connector import connect
from urllib3 import request


class MyModel:
    def __init__(self, info_database):
        self.stop_words = get_stop_words('vi')
        self.max_len = 150
        self.loaded_tokenizer = joblib.load('tokenizer.pkl')
        self.model = tf.keras.models.load_model('LSTM_model.h5')

        self.info_mysql = info_database
        self.labels = []

        self.conn = connect(host=self.info_mysql['server'], database=self.info_mysql['database'],
                            user=self.info_mysql['user'], password=self.info_mysql['password'])

        self.load_labels()

    def load_labels(self):
        sql = "SELECT * FROM model_lables"
        cur = self.conn.cursor()
        cur.execute(sql)
        for row in cur:
            self.labels.append({
                'id': row[0],
                'solution': row[1],
                'name': row[2],
                'type': row[3]
            })
        cur.close()

    def remove_stopword(self, words):
        words = words.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        filtered_text = ' '.join(filtered_words)
        return filtered_text

    def remove_punctuation(self, words):
        translator = str.maketrans('', '', string.punctuation)
        text_without_punct = words.translate(translator)
        return text_without_punct

    def preiction(self, content):
        content = content.lower()
        content = self.remove_punctuation(content)
        content = self.remove_stopword(content)

        X_new = pd.Series(data=[content])

        sequences_new = self.loaded_tokenizer.texts_to_sequences(X_new)
        sequences_matrix_new = tf.keras.preprocessing.sequence.pad_sequences(sequences_new, maxlen=self.max_len)

        predicted_probabilities = self.model.predict(sequences_matrix_new)

        return self.labels[np.argmax(predicted_probabilities)]
