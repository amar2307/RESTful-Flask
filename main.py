import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash,request
from security import auth,identity
from flask_jwt import JWT,jwt_required

app.secret_key='mukesh'
jwt=JWT(app,auth,identity)
@app.route('/add',methods=['POST'])
@jwt_required()
def add_user():
    try:
        _json = request.json
        _device=_json['id']
        _username=_json['username']
        _password=_json['password']
        _status=_json['status']
        _current=_json['current']
        _name = _json['name']
        _email = _json['email']
        _phone=_json['phone']
        if _username and _password and _device and _status and _current and _name and _email and _phone and request.method=='POST':
            sql = "INSERT INTO users2(UID,USERNAME,PASSWORD,STATUS,CURRENTTIME,NAME,EMAIL,PHONE_NUMBER) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (_device,_username,_password,_status,_current,_name,_email,_phone,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User added successfully!!!!')
            resp.status_code =200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()  

@app.route('/users')
@jwt_required()
def users():
    try:
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users2")
        rows=cursor.fetchall()
        resp=jsonify(rows)
        resp.status_code=200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/user/<int:id>')
@jwt_required()
def user(id):
    try:
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users2 WHERE UID=%s",id)
        row=cursor.fetchone()
        resp=jsonify(row)
        resp.status_code=200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/update',methods=['POST'])
def update_user():
    try:
        _json = request.json
        _user=_json['id']
        _username=_json['username']
        _password=_json['password']
        _status=_json['status']
        _current=_json['current']
        _name = _json['name']
        _email = _json['email']
        _phone=_json['phone']
        if _username and _password and _user and _status and _current and _name and _email and _phone and request.method=='POST':
            sql = "UPDATE users2 SET USERNAME=%s,PASSWORD=%s,STATUS=%s,CURRENTTIME=%s,NAME=%s,EMAIL=%s,PHONE_NUMBER=%s WHERE UID=%s"
            data = (_username,_password,_status,_current,_name,_email,_phone,_user,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Updated !!!!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()                
@app.route('/delete/<int:id>')
def delete_user(id):
    try:
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("DELETE FROM users2 WHERE UID=%s",(id,))
        conn.commit()
        resp=jsonify('Attention !!! DATA Deleted')
        resp.status_code=200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()        

@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message':'NOT FOUND:'+request.url,
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp

if __name__=="__main__":
    app.run(debug=True)