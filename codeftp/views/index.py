from flask import Flask,Blueprint,redirect,render_template,request,session
import pymysql
import os
from  ..utils import helper
inx=Blueprint('inx',__name__)
@inx.before_request
def process_before():
    if not session.get('user_info'):
        return redirect('/login')
    return None

@inx.route('/home')
def home():
    return render_template('layout.html')

@inx.route('/user_list')
def user_list():
    # conn=pymysql.Connection(host='127.0.0.1',user='root',password='123456',port=3306,database='codeftp')
    # cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute("select id,name,nickname from account")
    # data_list=cursor.fetchall()
    # cursor.close()
    # conn.close()
    data_list=helper.fetch_all("select id,name,nickname from account",[])
    return render_template('user_list.html',data_list=data_list)

@inx.route('/detail/<int:nid>')
def detail(nid):
    # conn=pymysql.Connection(host='127.0.0.1',user='root',password='123456',port=3306,database='codeftp')
    # cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute("select *from record where user_id=%s",(nid))
    # data=cursor.fetchall()
    # cursor.close()
    # conn.close()
    data=helper.fetch_all("select *from record where user_id=%s",(nid))
    xx=helper.fetch_one("select user_id from record where user_id=%s",(nid))
    nickname=helper.fetch_one("select nickname from account WHERE id=(select user_id from record where user_id=%s limit 1 )",(nid))
    return render_template('detail.html',data=data,nickname=nickname)

@inx.route('/upload',methods=['GET',"POST"])
def upload():
    try:
        if request.method=='GET':
            return render_template('upload.html')
        # from werkzeug.datastructures import FileStorage
        file_obj=request.files.get('code')
        name_ext=file_obj.filename.rsplit('.',maxsplit=1)
        if len(name_ext) !=2:
            return "请上传rar文件!"
        # if name_ext[1] !='rar':
        #     return "请上传rar文件"
        # file_path=os.path.join('files',file_obj.filename)
        # print(file_path)
        # file_obj.save(file_path)
        import shutil,uuid
        target_path=os.path.join('files',str(uuid.uuid4()))
        shutil._unpack_zipfile(file_obj.stream,target_path)
        total_num=0
        for base_path,folder_list,file_list in os.walk(target_path):
            for file_name in file_list:
                file_path=os.path.join(base_path,file_name)
                file_ext=file_path.rsplit('.',maxsplit=1)
                if len(file_ext) !=2:
                    continue
                if file_ext[1] !='py':
                    continue
                file_num=0
                with open(file_path,'rb') as f:
                    for line in f:
                        line=line.strip()
                        if not line:
                            continue
                        if line.startswith(b'#'):
                            continue
                        file_num +=1
                total_num +=file_num
    except Exception as e:
        return '请上传正确的文件格式'
    import datetime
    ctime=datetime.date.today()
    # conn=pymysql.Connection(host='127.0.0.1',port=3306,user='root',password='123456',database='codeftp')
    # cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute("select id from record where datetime=%s and user_id=%s",(ctime,session['user_info']['id']))
    # data=cursor.fetchall()
    # cursor.close()
    # conn.close()
    data=helper.fetch_all("select id from record where datetime=%s and user_id=%s",(ctime,session['user_info']['id']))
    if data >2:
        return "今天已上传"
    # conn = pymysql.Connection(host='127.0.0.1', port=3306, user='root', password='123456', database='codeftp')
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor.execute("insert into record(user_id,datetime,codeline) values(%s,%s,%s)",(session['user_info']['id'],ctime,total_num))
    # conn.commit()
    # cursor.close()
    # conn.close()
    helper.insert("insert into record(user_id,datetime,codeline) values(%s,%s,%s)",(session['user_info']['id'],ctime,total_num))

    return "上传成功"