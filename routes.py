from flask import render_template, request, redirect, url_for, make_response
from server import app 
import hashlib
import uuid 


'''
Purposly making our website vulnerable
'''
def lazy(*args):
    response = make_response(*args)
    response.headers["X-XSS-Protection"] = 0
    return response


'''
Storage of user login details 

user_db = { 
    "username" : {
        passwd: "password", 
        notes: [
            "note1", 
            "note2", 
        ]
    }
}

token_db = { 
    "token" : "usernm" 
}

Normally this would be stored within a database, NOT done like this. 

Token storing can be much better managed, but will be kept simple for the demo. 
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
        usernm = token_db[token]
        return lazy(render_template('index.html', username=usernm, cookie_value=token, notes=user_db[usernm]["notes"]))
 
    if request.method == "POST":
        usernm = request.form['name'] 
        passwd = request.form['password'] 
        passwd_hash = hashlib.md5((usernm + ":" + passwd).encode()).hexdigest()

        # Make new account
        if usernm not in user_db:
            user_db[usernm] = { 
                "passwd": passwd_hash,
                "notes": [],
            }
        elif user_db[usernm]["passwd"] != passwd_hash: 
            return lazy(render_template("login.html", error="true")) 

        token = uuid.uuid4().hex
        token_db[token] = usernm
        res = lazy(render_template('index.html', username=usernm, cookie_value=token, notes=[]))
        res.set_cookie('token', token, 60*60*24)
        return res

    return ":X"

'''
User adding new note to their dashboard
'''
@app.route('/post_note', methods=["POST"])
def post_note(): 
    token = request.cookies.get("token")
    if token not in token_db:
        return redirect(url_for("login"))
    
    note = request.form['note']
    usernm = token_db[token]
    user_db[usernm]["notes"].append(note)

    return lazy(render_template('index.html', cookie_value=token, notes=user_db[usernm]["notes"], ))



'''
User wants to be hacked 
'''
@app.route('/hack_me', methods=["GET"])
def hack_me(): 
    return lazy(render_template('hacked.html')) 