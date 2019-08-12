from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
import json

app = Flask(__name__)
mysql = MySQL()
CORS(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'fg'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

@app.route('/')
def get():
    cur = mysql.connect().cursor()
    cur.execute('''select nama from fg.fotografer''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'data' : r})

@app.route('/produk')
def getproduk():
    cur = mysql.connect().cursor()
    cur.execute('''select nama_produk from fg.produk''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'data' : r})

@app.route('/cek_jadwal/<tgl>')
def cek_tgl(tgl):
    cur = mysql.connect().cursor()
    cur.execute("SELECT * FROM fotografer WHERE id_fg NOT IN (SELECT id_fotografer FROM booking WHERE tgl_foto=%s)",tgl )
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'data' : r})
    # return tgl

@app.route('/pesan_addnama', methods=['POST'])
def pesan_addnama():
    if not request.json:
        abort(400)
    print (request.json)
    return json.dumps(request.json)

@app.route('/pesan_addemail', methods=['POST'])
def pesan_addnama():
    if not request.json:
        abort(400)
    print (request.json)
    return json.dumps(request.json)

@app.route('/pesan_addnohp', methods=['POST'])
def pesan_addnama():
    if not request.json:
        abort(400)
    print (request.json)
    return json.dumps(request.json)

if __name__ == '__main__':
    app.run()