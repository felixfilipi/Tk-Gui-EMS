import pymysql
con = pymysql.connect(db="EMPLOYEE_MANAGEMENT", user="root",passwd="root",
        host="localhost",port=3306,autocommit=True)
cur = con.cursor()
cur.execute("select * from EMPLOYEE")
data = cur.fetchall()
print(data[1][2])
