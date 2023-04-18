from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler


WSGIRequestHandler.protocol_version = "HTTP/1.1"

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'bastien'
app.config['MYSQL_PASSWORD'] = '123456Azerty'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)


@app.route('/livres', methods=['GET'])
def get_livres():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM livres''')
    result = cur.fetchall()
    livres = []
    for livre in result:
        livre_data = {}
        livre_data['id'] = livre[0]
        livre_data['FirstName'] = livre[1]
        livre_data['LastName'] = livre[2]
        livre_data['Title'] = livre[3]
        livre_data['Description'] = livre[4]
        livre_data['Image'] = livre[5]
        livres.append(livre_data)
    return jsonify(livres)


@app.route('/livres', methods=['POST'])
def add_livre():
    FirstName = request.json['FirstName']
    LastName = request.json['LastName']
    Title = request.json['Title']
    Description = request.json['Description']
    Image = request.json['Image']
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO livres(FirstName, LastName, Title, Description, Image) VALUES(%s, %s, %s, %s, %s)''',
                (FirstName, LastName, Title, Description, Image))
    mysql.connection.commit()
    return jsonify({'message': 'livre added successfully'})


@app.route('/livres/delete', methods=['DELETE'])
def delete_all_livres():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''DELETE FROM livres WHERE id NOT IN (1, 2)''')
        mysql.connection.commit()
    return


scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_all_livres, trigger='interval', minutes=1)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)