import pymysql.cursors  
# twine upload dist/*


class mysql(object): 
  
	def __init__(self, host, database, user, password, port=3306 ):
		# Connect to the database
		mysql.connection = pymysql.connect(host=host, database=database, user=user, password=password, port=port, 
		cursorclass=pymysql.cursors.DictCursor) 


	@classmethod
	def set(cls, sql, params = None):
		cur = cls.connection.cursor()
		cur.execute(sql, params)
		cls.connection.commit()
		return cur.rowcount
		cls.connection.close()
	
	@classmethod
	def get(cls, sql, params = None):  
		cur = cls.connection.cursor()
		cur.execute(sql, params)
		result = cur.fetchall() 
		return result
		cls.connection.close()

