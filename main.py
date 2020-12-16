import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash,request

@app.route('/add',methods=['POST'])
def add_user():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _json = request.json
        _username=_json['username']
        _password=_json['password']
        _device=_json['id']
        _status=_json['status']
        _current=_json['current']
        _name = _json['name']
        _email = _json['email']
        _phone=_json['phone']
        if _username and _password and _device and _status and _current and _name and _email and _phone and request.method=='POST':
            sql = "INSERT INTO users(USERNAME,PASSWORD,DEVICE_ID,STATUS,CURRENT,NAME,EMAIL,PHONE_NUMBER) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (_username,_password,_device,_status,_current,_name,_email,_phone,)
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
def users():
    try:
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")
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
def user(id):
    try:
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE DEVICE_ID=%s",id)
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
        #_id=request.args.get('id')
        _device=request.args.get('id')
        _username=request.args.get('username')
        _password=request.args.get('password')
        _status=request.args.get('status')
        _current=request.args.get('current')
        _name = request.args.get('name')
        _email = request.args.get('email')
        _phone=request.args.get('phone')
        if _username and _password and _device and _status and _current and _name and _email and _phone and request.method=='POST':
            sql = "UPDATE users SET USERNAME=%s, PASSWORD=%s, STATUS=%s,CURRENT=%s,NAME=%s,EMAIL=%s,PHONE_NUMBER=%s WHERE DEVICE_ID=(id)"
            data = (_username,_password,_status,_current,_name,_email,_phone,_device,)
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
        cursor.execute("DELETE FROM users WHERE DEVICE_ID=%s",(id,))
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
