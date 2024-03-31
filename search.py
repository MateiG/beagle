import json
import math
import os
import re
from collections import Counter
import difflib

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


def install_nltk_data():
    if not os.path.exists("./nltk_data"):
        os.makedirs("./nltk_data")
    nltk.download("punkt", download_dir="./nltk_data")
    nltk.download("stopwords", download_dir="./nltk_data")


install_nltk_data()
nltk.data.path.append("./nltk_data")


class BM25SearchEngine:
    def __init__(self, index_file):
        self.index_file = index_file
        self.documents = self.load_documents()  # List of dictionaries
        self.index, self.idf = self.build_index()

    def load_documents(self):
        if not os.path.exists(self.index_file):
            return []

        with open(self.index_file, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                raise ValueError("Index file is corrupt or in an invalid format")

    def store_documents(self):
        with open(self.index_file, "w") as file:
            json.dump(self.documents, file)

    def add_document(self, url, title, text):
        text = f"{title} {text}"
        for doc in self.documents:
            if doc["url"] == url:
                doc["title"] = title
                doc["text"] = text
                self.store_documents()
                self.index, self.idf = self.build_index()
                return

        document = {"url": url, "title": title, "text": text}
        self.documents.append(document)
        self.store_documents()
        self.index, self.idf = self.build_index()

    def delete_documnet(self, url):
        self.documents = [doc for doc in self.documents if doc["url"] != url]
        self.store_documents()
        self.index, self.idf = self.build_index()

    def tokenize(self, text):
        text = re.sub(r"\s+", " ", text).strip()
        text = text.lower()

        tokens = word_tokenize(text)
        tokens = [re.sub("[^a-zA-Z0-9]", "", token) for token in tokens]
        tokens = [token for token in tokens if token]

        stop_words = set(stopwords.words("english"))
        tokens = [token for token in tokens if token not in stop_words]

        porter = PorterStemmer()
        tokens = [porter.stem(token) for token in tokens]

        return tokens

    def build_index(self):
        index = {}
        df = {}
        for doc_id, doc in enumerate(self.documents):
            terms = self.tokenize(doc["text"])
            term_counts = Counter(terms)
            for term, count in term_counts.items():
                if term not in index:
                    index[term] = {}
                    df[term] = 0
                index[term][doc_id] = count
                df[term] += 1

        idf = {
            term: math.log((len(self.documents) + 1) / (df_count + 1)) + 1
            for term, df_count in df.items()
        }
        return index, idf

    def compute_bm25_score(self, query, doc_id, avgdl, k1=1.5, b=0.75):
        score = 0
        doc_length = len(self.tokenize(self.documents[doc_id]["text"]))

        close_query_terms = []
        for term in query:
            close_query_terms.append(
                difflib.get_close_matches(term, self.index.keys(), n=1)[0]
            )
        close_query_terms = list(set(close_query_terms))

        for term in close_query_terms:
            if term in self.index:
                tf = self.index[term].get(doc_id, 0)
                idf = self.idf.get(term, 0)
                score += (
                    idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_length / avgdl))
                )
        return score

    def search(self, query_text, limit=10):
        if not self.documents:
            return []

        query = self.tokenize(query_text)
        avgdl = sum(len(self.tokenize(doc["text"])) for doc in self.documents) / len(
            self.documents
        )
        scores = {
            doc_id: self.compute_bm25_score(query, doc_id, avgdl)
            for doc_id in range(len(self.documents))
        }
        ranked_doc_ids = sorted(scores, key=scores.get, reverse=True)[:limit]
        return [
            {**self.documents[doc_id], "score": scores[doc_id]}
            for doc_id in ranked_doc_ids
        ]
