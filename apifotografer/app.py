from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import mysql.connector
import json

app = Flask(__name__)
CORS(app)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="password",
  database="fg"
)
cur = mydb.cursor()

@app.route('/')
def get():
    cur.execute('''select nama from fg.fotografer''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'data' : r})

@app.route('/produk')
def getproduk():
    cur.execute('''select id_produk,nama_produk from fg.produk''')
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    print(r)
    return jsonify({'data' : r})

@app.route('/cek_jadwal/<tgl>')
def cek_tgl(tgl):
    sql = "SELECT id_fg FROM fotografer WHERE id_fg IN (SELECT id_fotografer FROM booking WHERE tgl_foto='%s')"
    print(sql%tgl)
    cur.execute(sql%tgl)
    r = cur.fetchall()
    print(len(r))
    sql = "select count(id_fg) from fotografer"
    cur.execute(sql)
    count = cur.fetchall()
    for c in count:
        pass
    if len(r) == c[0]:
        return jsonify({'data' : "penuh"})
    else:
        cur.execute("select last_insert_id()")
        id = cur.fetchall()
        for x in id:
            print(x[0])
        sql = "UPDATE booking set tgl_boking = now(),tgl_foto='%s' where id_booking=%s"
        print(sql%(tgl,x[0]))
        cur.execute(sql%(tgl,x[0]))
        mydb.commit()
        return jsonify({'data' : "masih"})
    # return tgl

@app.route('/pesan_addnama', methods=['POST'])
def pesan_addnama():
    if not request.json:
        abort(400)
    nama = request.json['param']
    print (nama[0])
    sql = "insert into pemesan (nama) values ('%s')"
    print(sql%nama[0])
    cur.execute(sql%nama[0])
    mydb.commit()
    return jsonify({'data' : 'berhasil'})

@app.route('/booking/<id>')
def booking(id):
    sql = "INSERT INTO booking (id_produk) VALUES (%d)"
    val = (int(id))
    print(sql%val)
    cur.execute(sql% val)
    mydb.commit()
    return jsonify({'data' : 'berhasil'})

@app.route('/pesan_addnohp', methods=['POST'])
def pesan_addnoh():
    if not request.json:
        abort(400)
    print (request.json)
    return json.dumps(request.json)

if __name__ == '__main__':
    app.run(debug=True)