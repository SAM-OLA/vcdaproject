import psycopg2
from flask import request
import sqlite3

def connection():
    connn = psycopg2.connect(database="victoryestate", 
                        user="postgres", 
                        password="postgres", 
                        host="13.62.19.232", port="5432")  #127.0.0.1   16.171.31.3
    return connn

def connectionlite():
    connn = sqlite3.connect("victoryestate.db")
    return connn

