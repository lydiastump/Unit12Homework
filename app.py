from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars2

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def home():
    mars_data=mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)




@app.route("/scrape")

def scraper():
    mars_data = mongo.db.mars_data
    mars_scrape = scrape_mars2.scrape()
    mars_data.update({}, mars_scrape, upsert=True)

    return redirect("/", code=302)




if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5001)
