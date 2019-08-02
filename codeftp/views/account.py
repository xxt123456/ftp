import pymysql
from ..utils import helper
from flask import Blueprint,render_template,Flask,request,redirect,session
account=Blueprint('account',__name__)
@account.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    user=request.form.get('user')
    pwd=request.form.get('pwd')
    # conn=pymysql.Connection(host='127.0.0.1',user='root',password='123456',port=3306,database='codeftp')
    # cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute("select * from account where name=%s and password=%s",(user,pwd))
    # data=cursor.fetchone()
    # cursor.close()
    # conn.close()
    data=helper.fetch_one("select * from account where name=%s and password=%s",(user,pwd))
    if not data:
        return render_template('login.html',error="用户名或密码错误")
    session['user_info']={'id':data['id'],'nickname':data['nickname']}
    return redirect('/home')
@account.route('/logout')
def logout():
    if 'user_info' in session:
        del session['user_info']
    return redirect('login')

