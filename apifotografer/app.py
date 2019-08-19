from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import mysql.connector
import json
import random

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

@app.route('/booking/<id>')
def booking(id):
    sql = "INSERT INTO booking (id_produk) VALUES (%d)"
    val = (int(id))
    print(sql%val)
    cur.execute(sql% val)
    mydb.commit()
    return jsonify({'data' : 'berhasil'})

@app.route('/harga/<id>')
def harga(id):
    sql = "select harga_produk from produk where id_produk=%d"
    val = (int(id))
    print(sql%val)
    cur.execute(sql% val)
    harga = cur.fetchall()
    for x in harga:
        print(x[0])
    return jsonify({'data' : x[0]})

@app.route('/cek_jadwal/<tgl>')
def cek_tgl(tgl):
    sql = "SELECT id_fg FROM fotografer WHERE id_fg NOT IN (SELECT id_fotografer FROM booking WHERE tgl_foto='%s')"
    print(sql%tgl)
    cur.execute(sql%tgl)
    r = cur.fetchall()
    print(r)
    try:
        a = random.choice(r[0])
    except IndexError:
        print("Erorr index")
    if len(r) == 0:
        return jsonify({'data' : "penuh"})
    else:
        cur.execute("select last_insert_id()")
        id = cur.fetchall()
        for x in id:
            print(x[0])
        sql = "UPDATE booking set id_fotografer = %s, tgl_boking = now(),tgl_foto='%s' where id_booking=%s"
        print(sql%(a,tgl,x[0]))
        cur.execute(sql%(a,tgl,x[0]))
        mydb.commit()
        return jsonify({'data' : "masih"})

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

@app.route('/add_data', methods=['POST'])
def pesan_addnoh():
    if not request.json:
        abort(400)
    print (request.json)
    sql = "SELECT id FROM pemesan ORDER BY id DESC LIMIT 1"
    cur.execute(sql)
    id = cur.fetchall()
    for id_fg in id:
        pass
    data = request.json
    sql = "update pemesan set email='%s', no_hp='%s' where id=%s"
    print(sql%(data['email'],data['nohp'],id_fg[0]))
    cur.execute(sql%(data['email'],data['nohp'],id_fg[0]))
    mydb.commit()

    sql = "SELECT id_booking FROM booking ORDER BY id_booking DESC LIMIT 1"
    cur.execute(sql)
    id_bk = cur.fetchall()
    for i in id_bk:
        pass
    sql = "update booking set id_pemesan=%s where id_booking=%s"
    print(sql%(id_fg[0],i[0]))
    cur.execute(sql%(id_fg[0],i[0]))
    mydb.commit()
    return jsonify({'data' : 'berhasil'})

if __name__ == '__main__':
    app.run(debug=True)