from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sqlite3, json

app = Flask(__name__)
CORS(app, support_credentials=True)

email="admin@admin.com"
password="a29c57c6894dee6e8251510d58c07078ee3f49bf"

@app.route("/login", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_logins():
	if request.args.get('email')==email:
		if request.args.get('password')==password:
			return 'matched'
	return 'notmatched'
    		
def new_id():
	conn = sqlite3.connect('employee.db')
	crsr = conn.cursor()
	crsr.execute('SELECT MAX(id) FROM emp_details')
	max_value = crsr.fetchall()
	ans = str(max_value[0])
	conn.close()
	return ans[1]

@app.route("/emp", methods=["GET"])
def get_emp():
	connection = sqlite3.connect('employee.db')
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM emp_details')
	ans = cursor.fetchall()
	connection.close()
	return json.dumps(ans)
	
@app.route("/emp", methods=["POST"])
def add_emp():
	emp = request.get_json()
	emp_new_id = new_id()
	idv = str(int(emp_new_id) + 1)
	connection = sqlite3.connect('employee.db')
	cursor = connection.cursor()
	mysql_cmd = 'INSERT INTO emp_details VALUES('+idv+', "'+emp['name']+'", "'+emp['designation']+'", "'+emp['address']+'")'
	cursor.execute(mysql_cmd)
	connection.commit()
	connection.close()
	return "201 CREATED - New record created successfully with id "+idv+"."
	
@app.route("/emp", methods=["PUT"])
def update_emp():
	emp = request.get_json()
	connection = sqlite3.connect('employee.db')
	cursor = connection.cursor()
	mysql_cmd = 'UPDATE emp_details SET name = "'+emp['name']+'", designation = "'+emp['designation']+'", address = "'+emp['address']+'" WHERE id = '+emp['id']
	cursor.execute(mysql_cmd)
	connection.commit()
	connection.close()
	return "200 OK - Record updated successfully."
	
@app.route('/emp', methods=['DELETE'])
def emp_del():
	emp = request.get_json()
	connection = sqlite3.connect('employee.db')
	cursor = connection.cursor()
	sql_cmd = 'DELETE FROM emp_details WHERE id = '+emp['id']
	cursor.execute(sql_cmd)
	connection.commit()
	connection.close()
	return "200 OK - Record deleted successfully."

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)


