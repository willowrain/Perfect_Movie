import imdb_scraper
import get_ids

import mysql.connector

#connect to database

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Werhd9002!',
    database = 'movies'
)


#create database cursor
mycursor = mydb.cursor()
#execute database creation
mycursor.execute("CREATE DATABASE movies")

mycursor.execute("CREATE TABLE movies")

#close the cursor
mycursor.close()
#close the connection
mydb.close()

