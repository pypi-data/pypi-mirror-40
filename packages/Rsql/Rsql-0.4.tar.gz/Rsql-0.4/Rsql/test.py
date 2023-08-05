from Rmysql import mysql

db = mysql('127.0.0.1', 'test', 'root', 'root', 3306)
print(db.get("SELECT * FROM users"))  