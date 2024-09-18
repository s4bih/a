

from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import json

from werkzeug.utils import redirect

app = Flask(__name__)
with open('config.json', 'r') as c:
    params = json.load(c)["parameters"]




if params["local_server"]:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']

app.config['SECRET_KEY'] = params['secret_key']

app.config['SECRET_KEY']
db=SQLAlchemy(app)


class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    tempattanggallahir = db.Column(db.String(50), nullable=False)
    alamat = db.Column(db.String(100), nullable=False)
    jeniskelamin = db.Column(db.String(50), nullable=False)
    namaibu = db.Column(db.String(50), nullable=False)
    namabapak = db.Column(db.String(50), nullable=False)

@app.route("/",methods=['GET'])

def siswa():

    s = Siswa.query.all()
    print(s)

    return render_template('crud.html',s=s)

@app.route("/add",methods=['GET','POST'])
def add():

    if request.method=='POST':
        id = request.form.get('id')
        nama = request.form.get('nama')
        tempattanggallahir = request.form.get('tempattanggallahir')
        alamat = request.form.get('alamat')
        jeniskelamin = request.form.get('jeniskelamin')
        namaibu = request.form.get('nm.ibu')
        namabapak = request.form.get('nm.bapak')
        s = Siswa(id=id,nama=nama,tempattanggallahir=tempattanggallahir,alamat=alamat,jeniskelamin=jeniskelamin,namaibu=namaibu,namabapak=namabapak)
        db.session.add(s)
        db.session.commit()
    return render_template('add.html')


if __name__ == "__main__":
    app.run()
    debug = True