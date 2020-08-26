from flask import render_template, request, redirect, url_for, make_response
from server import app 
import hashlib
import uuid 
import src.create_database


'''
Purposly making our website vulnerable
'''
def lazy(*args):
    response = make_response(*args)
    response.headers["X-XSS-Protection"] = 0
    return response


'''
Storage of user login details 

db = { 
    "username" : {
        passwd: "password", 
        msgs: [
            "note1", 
            "note2", 
        ]
    }
}

token_db = { 
    "token" : usernm 
}

Normally this would be stored within a database, NOT done like this. 
'''
user_db = {}
token_db = {} 


''' 
Landing page 
''' 
@app.route("/", methods=["POST", "GET"])
def login(): 
    token = request.cookies.get('token')
    
    '''
    Unknown user
    '''
    if token not in token_db:
        return render_template('login.html') 
    return redirect(url_for("main"))

'''
Index
'''
@app.route('/main', methods=["GET", "POST"])
def main(): 
    if request.method == "GET":
        token = request.cookies.get('token')
        if token not in token_db:
            return redirect(url_for("login"))
        return lazy(render_template('index.html', cookie_value=token, msgs=user_db[usr][notes])
 
    if request.method == "POST":
        usernm = request.form['name'] 
        passwd = request.form['password'] 
        passwd_hash = hashlib.md5((name + ":" + password).encode()).hexdigest()

        # Make new account
        if usernm not in user_db:
            user_db[usernm]["passwd"] = passwd_hash
            user_db[usernm]["msgs"] = [] 
        elif user_db[usernm]["passwd"] != passwd_hash: 
            return lazy(render_template("login.html", error="true")) 

        token = uuid.uuid4() 
        res = lazy(redirect(url_for("main", username=usernm)))
        res.set_cookie('token', token, 60*60*24)
        return res

    return ":X"

'''
User adding new msg to their dashboard
'''
@app.route('/post_msg', methods=["POST"])
def post_msg(): 
    token = request.cookies.get("token")

    if token not in user_db:
        return redirect(url_for("login"))
    
    msg = request.form['msg']
    usr = token_db[token]
    user_db[usr][notes].append(msg)

    return lazy(render_template('index.html', cookie_value=token, msgs=user_db[usr][notes]))




    