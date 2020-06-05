from datetime import time

from flask import Flask, render_template, request, json, session, make_response
from redis import Redis, ReadOnlyError
import time

app = Flask(__name__)
app.secret_key = 'fhierhgtoi34tuqp'
#
# SESSION_EXPIRY_MINUTES = 60
# SESSION_COOKIE_NAME = 'session'

def redisconnect():
    import redis
    r=redis.Redis("localhost", charset="utf-8", decode_responses=True)
    return r

# def utctimestamp_by_second(utc_date_time):
#     return int((utc_date_time.replace(tzinfo=time.timezone.utc))).timestamp()

@app.route('/admin')
def admin():
    return render_template('index.html',status='status')
    # return "Hello"
@app.route('/admin/createuser')
def admin_create_user():
    return render_template('admin.html', status='status')

@app.route('/backend/create_user', methods=['POST'])
def create_user():
    import json
    data = json.loads(request.data.decode('utf-8'))
    user = data['user']
    password = data['password']
    if user:
        df=dict()
        df[user]=dict()
        df[user]["password"]=password
        df=json.dumps(df)
        r=redisconnect()
        r.set(user,df)
        return user
    else:
        return "error"

@app.route('/user/login')
def login():
    # session.pop('user',None)
    return render_template('login.html',status='status')

# @app.route('/setcookie', methods=['POST'])
# def setcookie():
#     if request.method =='POST':
#         user = request.form['user']
#
#         resp = make_response()
#         resp.set_cookie('user', user)
#
#         return resp


@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('user')
    return name



@app.route('/user/home',methods=['GET'])
def user_home():
    if request.method=='GET':
        user = request.args['val']
        session['user'] = user
    return render_template('userhome.html',user=user)
    # return render_template('userhome.html', status='status')



@app.route('/backend/user_login', methods=['POST'])
def check_user():
    import json
    data = json.loads(request.data.decode('utf-8'))
    user = data['user']
    password = data['password']
    # if request.method == 'POST':
    #     user = request.form['user']
    #     password = request.form['password']
    if user and password:
        r = redisconnect()
        if r.get(user):
            d = json.loads(r.get(user))
            if d[user]['password'] == password:
                return "Suceess"
                # return render_template('userhome.html', status='status')
            else:
                return "error"
    else:
        return "error"

@app.route('/backend/user_home', methods=['POST'])
def create_post():
    import json
    data = json.loads(request.data.decode('utf-8'))
    user = data['user']
    upost = data['upost']
    r = redisconnect()
    if user:
        t = time.time()
        df=dict()
        df['user']=user
        df[upost]=dict()
        df[upost]['post']=upost
        df[upost]['time']=t
        df=json.dumps(df)
        r.set(user,df)
        info = {upost:{'post':upost,'time':t}}
        return info
    else:
        return "error"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
