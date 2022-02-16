from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
#URI is uniform resouce identifier, similar to URL
#localhost designates the local machine as the server, port 27017

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)
#identifies mars as the path to the mars collection in database
#render_template returns HTML format
#mars = mars, use the mars collection in MongoDB

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)
#@app.route - route to find the page, then what we do there
#function defines scrape, then directs it to the mars db in Mongo
#mars_data holds the information we scrape in the page, note scrape_all
#update_one adds another dictionary to the Mongo DB
#$set is the tag as a key, then the value

if __name__ == "__main__":
   app.run()
#standard code to run Flask 