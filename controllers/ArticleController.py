from typing import List
from fastapi import FastAPI, HTTPException,status
from elasticsearch_connect import get_elasticsearch
from datetime import date, datetime
import requests
from sqlalchemy.orm import Session
from models.Article import Article
from models.Auteur import Auteur
from models.Institution import Institution
from models.Mot_Cle import Mot_Cle
from models.Institution import Institution
from utils.HTTPResponse import HTTPResponse
from utils.ExtendedArticle import ExtendedArticle

##Elasticsearch_connection
es = get_elasticsearch()
index_name="articles"

try:
    if es.ping():
        print("Connected to Elasticsearch")
    else:
        print("Unable to connect to Elasticsearch")
except Exception as e:
    print(f"Error connecting to Elasticsearch: {str(e)}")

class ArticleController():
    def __init__(self):
        self.elasticsearch = get_elasticsearch()
        try:
            if es.ping():
                print("Connected to Elasticsearch")
            else:
                print("Unable to connect to Elasticsearch")
        except Exception as e:
            print(f"Error connecting to Elasticsearch: {str(e)}")

    def index_article(article: Article):
        try:
            es.index(index=index_name, body=article)
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article indexed successfully")
        except Exception as e:
            error_message = f"Error indexing Article: {str(e)}"
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)

    def delete_indexed_article(Article_Id):
        if es.exists(index=index_name, id=Article_Id):
            es.delete(index=index_name, id=Article_Id)
            raise HTTPResponse(status_code=status.HTTP_200_OK, detail="Article  deleted successfully from elasticsearch")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No article found with this id in elasticsearch")   
        
    def get_all_indexed_articles():
        search_query = {"query": {"match_all": {}}}
        result = es.search(index=index_name, body=search_query)
        articles = result['hits']['hits']
        return articles
    
    # Elasticsearch query to search in the title, keywords, authors, and full text
    def search_articles(query_terms):
        query = {
            "query": {
                "multi_match": {
                    "query": query_terms,
                    "fields": ["Titre", "Mots_Cles", "Auteurs", "Texte"]
                }
            }
        }
    
        try:
            response = es.search(index=index_name, body=query)
            hits = response.get("hits", {}).get("hits", [])
            articles = []

            for hit in hits:
                ##source = hit.get("_source", {}) //hadi ki nkono nhawso 3la les info ta3 l'article (wech kayn f _source)
                articles.append(hit)
            #sort the search results in reverse chronological order
            sorted_articles = sorted(articles, 
                                     key=lambda x: datetime.strptime(x["_source"].get("Date_Publication", ""), "%Y-%m-%d").date(), 
                                     reverse=True)
            return sorted_articles
        except Exception as e:
            print(f"Error searching articles: {str(e)}")
            raise

    # Filtres 
    def apply_filters(
        self,
        articles,
        Mots_Cles: List[str] = None,
        Auteurs: List[str] = None,
        Institutions: List[str] = None,
        start_date: date = None,
        end_date: date = None,
    ):
        filtered_articles = [
            article for article in articles
            if (
                (not Mots_Cles or any(Mots_Cle.lower() in map(str.lower, article["_source"].get("Mots_Cles", [])) for Mots_Cle in Mots_Cles)) and
                (not Auteurs or any(Auteur.lower() in map(str.lower, article["_source"].get("Auteurs", [])) for Auteur in Auteurs)) and
                (not Institutions or any(Institution.lower() in map(str.lower, article["_source"].get("Institutions", [])) for Institution in Institutions)) and
                (not start_date or datetime.strptime(article["_source"].get("Date_Publication"), "%Y-%m-%d").date() >= start_date) and
                (not end_date or datetime.strptime(article["_source"].get("Date_Publication"), "%Y-%m-%d").date() <= end_date)
            )
        ]

        return filtered_articles

    # The search and filtre function 
    def search_and_filter_articles(
        self,
        query_terms: str,
        Mots_Cles: List[str] = None,
        Auteurs: List[str] = None,
        Institutions: List[str] = None,
        start_date: date = None,
        end_date: date = None,
    ):
        search_results = self.search_articles(query_terms)
        filtered_results = self.apply_filters(
            self,
            search_results,
            Mots_Cles=Mots_Cles,
            Auteurs=Auteurs,
            Institutions=Institutions,
            start_date=start_date,
            end_date=end_date,
        )
        return filtered_results