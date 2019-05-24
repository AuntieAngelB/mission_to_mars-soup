from flask import Flask, render_template, redirect, url_for
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__, template_folder='templates')

conn = 'mongodb://localhost:27017/'
client = pymongo.MongoClient(conn)
db = client.mars
collection = db.mars_collection

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars = collection.find_one()
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_all()
    collection.update({}, mars_data, upsert=True)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)