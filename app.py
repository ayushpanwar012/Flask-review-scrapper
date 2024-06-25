from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
app = Flask(__name__)


@app.route("/", methods = ["GET"])
def introPage():
    return render_template('index.html')


@app.route("/review-results", methods = ["GET", "POST"])
def resultPage():
    if request.method == "POST":
        try:
            searchString = request.form['content'].replace(" ", "+")
            flipkart_url = "https://www.flipkart.com"
            search_query= "/search?q="
            uclient=uReq(flipkart_url+search_query+searchString)
            bdata=uclient.read()
            flipkart_html=bs(bdata,"html.parser")
            priceboxes = flipkart_html.findAll("div", {"class": "Nx9bqj _4b5DiR"})
            price = priceboxes[0].text
            nameboxes = flipkart_html.findAll("div",{"class":"KzDlHZ"})
            product_name = nameboxes[0].text
            link=flipkart_html.findAll("div",{"class":"cPHDOP col-12-12"})
            prod_link = flipkart_url + link[2].div.div.div.a['href']
            product_page=uReq(prod_link)
            pdata = product_page.read()
            product_html = bs(pdata, "html.parser")
            comment_boxes=product_html.findAll("div",{"class":"col EPCmJX"})
            reviews = []
            for i in range(0, len(comment_boxes)):
                try:
                    rating = comment_boxes[i].div.div.text
                except:
                    rating = "No rating"
                try:
                    comment_heading = comment_boxes[i].div.p.text
                except:
                    comment_heading = "No Comment Heading"
                try:
                    comment = comment_boxes[i].findAll("div",{"class":""})[0].div.text
                except:
                    comment = "No Comments 🤐🤐🤐"
                try:
                    name = comment_boxes[i].findAll("div",{"class":"row gHqwa8"})[0].div.p.text
                except:
                    name = "No Name 😶😶"

                mydict = {"Product Name": product_name, "Price": price, "Rating" : rating, "Comment Head": comment_heading, "Comment": comment, "Commented By": name}
                reviews.append(mydict)

            return render_template("result.html", reviews = reviews[0:(len(reviews)-1)]) 
            # return json.dumps(reviews)    
        except Exception as e:
            print(e)

    else:
        render_template("index.html")        

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)