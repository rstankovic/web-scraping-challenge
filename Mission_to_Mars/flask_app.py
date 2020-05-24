from flask import Flask, jsonify, render_template, redirect, url_for
import scrape_mars
import pymongo
import json

###############
# Flask Setup
##############

app = Flask(__name__)

#################
# pymongo setup
#################
conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.mars_db

data = scrape_mars.scrape_master()
db.mars_data.insert_one(data)

################
# Flask Routes
###############

@app.route('/scrape_mars/json/')
def get_json():
    main_dictionary = scrape_mars.scrape_master()

    return jsonify(main_dictionary)


@app.route('/')
def main():
    return render_template('index.html',final_dict = data)


################
if __name__ == '__main__':
    app.run(debug = True)