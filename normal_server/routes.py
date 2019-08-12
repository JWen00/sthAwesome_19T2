from flask import render_template, request, redirect, url_for, make_response
from server import app 
import hashlib
import src.create_database


def lazy(*args):
    response = make_response(*args)
    response.headers["X-XSS-Protection"] = 0
    return response

'''
Landing page 
''' 
cookie_map = {}
@app.route("/", methods=["POST", "GET"])
def index(): 
    token = request.cookies.get('token')
    if token not in cookie_map:
        return render_template('index.html') 
    return redirect(url_for("main_page"))

@app.route('/main_page', methods=["GET", "POST"])
def main_page(): 
    if request.method == "GET":
        token = request.cookies.get('token')
        if token not in cookie_map:
            return redirect(url_for("index"))

        notification = request.args.get("notification")

        return lazy(render_template('login_success.html', cookie_value=token, msgs=cookie_map[token], notification = notification))
    
    elif request.method == "POST":
        # Make an account / login
        name = request.form['name'] 
        password = request.form['password'] 
        hashed_token = hashlib.md5((name + ":" + password).encode()).hexdigest()

        cookie_map[hashed_token] = ["Hello"]

        res = lazy(redirect(url_for("main_page", notification = "Welcome!")))
        res.set_cookie('token', hashed_token, 60*60*24)
        return res

    return ":X"

@app.route('/post_msg', methods=["POST"])
def post_msg(): 
    token = request.cookies.get("token")
    if token not in cookie_map:
        return ":("
    
    msg = request.form['msg']
    cookie_map[token].append(msg)

    return lazy(render_template('login_success.html', cookie_value=token, msgs=cookie_map[token]))
