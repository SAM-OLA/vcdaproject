import psycopg2
from flask import request
import sqlite3

from traitlets import This
errorrr = "No Error"
def connection():

        try:
            connn = psycopg2.connect(database="victoryestate", 
                        user="postgres", 
                        password="Sqlserver!2", #  postgres Sqlserver!2
                        host="/cloudsql/project-4c43f2db-b2dc-47f4-a89:us-central1:victorydb")  #   10.0.2.41
            return connn
        except Exception as ee:
            print(f"An error occurred: {str(ee)}")
            errorrr = str(ee)
            return None, errorrr


def connectionlite():
    connn = sqlite3.connect("victoryestate.db")
    return connn

