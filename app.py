
#flask setup
from flask import Flask, render_template, redirect
app = Flask(__name__)

#Mongo DB connection with mLab
import pymongo
from pymongo import MongoClient

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn) 

db = client.mars_mission_webscrape
collection = db.mars_scrape
# print("======> Pre-flask initialization")
# print(collection)


# scrape function
from scrape_mars import scrape

@app.route("/")
def home():
    scrape_dict = collection.find_one()
    print("====> In the / route")
    print(scrape_dict)
    return render_template("indexmars.html", mars=scrape_dict)
    # return render_template("indexmars.html")

@app.route("/scrape")
def reload():
    mars_dict = scrape()
    collection.update({"id": 1}, {"$set": mars_dict}, upsert = True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == '__main__':
    app.run()