import psycopg2
from flask import request

def connection():
    connn = psycopg2.connect(database="victoryestate", 
                        user="postgres", 
                        password="postgres", 
                        host="localhost", port="5432")
    return connn

