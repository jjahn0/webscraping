from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_craigslist

app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings_data = scrape_craigslist.scrape()
    listings.update(
        {},
        listings_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
