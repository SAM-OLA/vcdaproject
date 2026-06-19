import psycopg2
from flask import request
import sqlite3


errorrr = "No Error"
def connection():

        try:
            connn = psycopg2.connect(database="victoryestate", 
                        user="postgres", 
                        password="postgres", #  postgres Sqlserver!2
                        host="127.0.0.1")  #   10.0.2.41
            return connn
        except Exception as ee:
            print(f"An error occurred: {str(ee)}")
            errorrr = str(ee)
            return None

def connect_error():
    error_string = errorrr
    return  error_string

def connectionlite():
    connn = sqlite3.connect("victoryestate.db")
    return connn

