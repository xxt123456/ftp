import pymysql
conn = pymysql.Connection(host='127.0.0.1', user='root', password='123456', port=3306, database='codeftp')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute("select * from account")
data_list = cursor.fetchall()
print(data_list)
cursor.close()
conn.close()