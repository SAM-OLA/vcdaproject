import psycopg2
from flask import request
import sqlite3

def connection():

        try:
            connn = psycopg2.connect(database="victoryestate", 
                        user="postgres", 
                        password="Sqlserver!2", 
                        host="10.0.2.201", port="5432")  #127.0.0.1  
            return connn
        except Exception as ee:
            print(f"An error occurred: {str(ee)}")
            return None
def connectionlite():
    connn = sqlite3.connect("victoryestate.db")
    return connn

