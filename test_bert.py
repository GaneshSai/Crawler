import seaborn as sns
from sklearn.metrics import pairwise
from sentence_transformers import SentenceTransformer
import tensorflow as tf
import tensorflow_hub as hub
from text_cleaning import *
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import csv
from new_crawler import sbert_model
import configparser

config = configparser.ConfigParser()
config.read("listnames_as_tuple.ini")
all_the_lists = config.items("lists")
for list_names, list_values in all_the_lists:
# sbert_model = SentenceTransformer("bert-base-nli-mean-tokens") # Model being loaded...


def most_similar(doc_id, similarity_matrix, matrix):
    # Finding similarity if Cosine similarity is chosen:
    if matrix == "Cosine Similarity":
        similar_ix = np.argsort(similarity_matrix[doc_id])[::-1]

    for ix in similar_ix:
        if ix == doc_id:
            continue
        return({similarity_matrix[doc_id][ix]})


def bert(text, url):
    text = text
    config = configparser.ConfigParser()
    config.read("listnames_as_tuple.ini")
    all_the_lists = config.items("lists")
    for list_names, list_values in all_the_lists:
        text_compared_with = list_values
        similariy_finder = [text, text_compared_with]
        documents_df = pd.DataFrame(similariy_finder, columns=["similariy_finder"])
        #removing stopwords and cleaning the text...
        stop_words_l = stopwords.words("english")
        documents_df["documents_cleaned"] = documents_df.similariy_finder.apply(
            lambda x: " ".join(
                re.sub(r"[^a-zA-Z]", " ", w).lower()
                for w in x.split()
                if re.sub(r"[^a-zA-Z]", " ", w).lower() not in stop_words_l
            )
        )
        #creating vector using the loaded model...
        document_embeddings = sbert_model.encode(documents_df["documents_cleaned"])
        pairwise_similarities = cosine_similarity(document_embeddings)
        score = most_similar(0, pairwise_similarities, "Cosine Similarity")
    with open('Similarity.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([url, score])