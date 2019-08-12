from flask import render_template, request, redirect, url_for, make_response
from server import app 
import hashlib


'''
Landing page 
''' 
@app.route("/", methods=["GET"])
def index(): 
    token = request.cookies.get('token')
    if token not in cookie_map:
        return redirect(url_for("main_page"))
    return render_template('index.html') 

@app.route('/main_page', methods=["GET", "POST"])
def main_page(): 
    if request.method == "GET":

    elif request.method == "POST":


    return ":X"
