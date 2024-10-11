

from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import json



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

class Sekolah(db.Model):
    sekolah=db.Column(db.String(100),primary_key=True)
    jumlah_siswa=db.Column(db.Integer,nullable=False)
    kabupaten=db.Column(db.String(150),nullable=False)
    kecamatan=db.Column(db.String(150),nullable=False)
    alamat_sekolah=db.Column(db.String(200),nullable=False)
class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    tempattanggallahir = db.Column(db.String(50), nullable=False)
    alamat = db.Column(db.String(100), nullable=False)
    jeniskelamin = db.Column(db.String(50), nullable=False)
    namaibu = db.Column(db.String(50), nullable=True)
    namabapak = db.Column(db.String(50), nullable=True)
    def __init__(self,nama,tempattanggallahir,alamat,jeniskelamin,namaibu,namabapak):
        self.nama = nama
        self.tempattanggallahir = tempattanggallahir
        self.alamat = alamat
        self.jeniskelamin = jeniskelamin
        self.namaibu = namaibu
        self.namabapak = namabapak

@app.route("/",methods=['GET'])

def sekolah():

    Sis=Siswa.query.all()
    s=Sekolah.query.all()
    return render_template('crud.html',s=s,Sis=Sis)



@app.route("/add",methods=['GET','POST'])
def add():
    print("ye",request.method)
    print("ya",request.form)
    if request.method == 'POST':
        print("ye")
        nama = request.form.get('nama')


        tempattanggallahir = request.form.get('tempattanggallahir')
        alamat = request.form.get('alamat')
        jeniskelamin = request.form.get('jeniskelamin')
        namaibu = request.form.get('namaibu')
        namabapak = request.form.get('namabapak')
        s = Siswa(nama=nama,tempattanggallahir=tempattanggallahir,alamat=alamat,jeniskelamin=jeniskelamin,namaibu=namaibu,namabapak=namabapak)
        db.session.add(s)
        db.session.commit()
        print("ye")
        return redirect(url_for('siswa'))
    return render_template('add.html',params=params)



@app.route("/delete/<string:post_id>", methods=['GET', 'POST'])
def delete(post_id):
    post = Siswa.query.filter_by(id=post_id).first()
    if post is None:
        return "Post not found", 404
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('siswa'))

@app.route("/update/<string:post_id>", methods=['GET', 'POST'])
def update(post_id):
    post = Siswa.query.filter_by(id=post_id).first()
    if post is None:
        return "Post tidak ditemukan", 404

    if request.method == 'POST':
        try:
            nnama = request.form.get('nama')
            ntempattanggallahir = request.form.get('tempattanggallahir')
            nalamat = request.form.get('alamat')
            njeniskelamin = request.form.get('jeniskelamin')
            nnamaibu = request.form.get('namaibu')
            nnamabapak = request.form.get('namabapak')

            # Validasi form
            if not all([nnama, ntempattanggallahir, nalamat, njeniskelamin, nnamaibu, nnamabapak]):
                return "Form tidak lengkap", 400

            post.nama = nnama
            post.tempattanggallahir = ntempattanggallahir
            post.alamat = nalamat
            post.jeniskelamin = njeniskelamin
            post.namaibu = nnamaibu
            post.namabapak = nnamabapak

            db.session.commit()
            return redirect(url_for('siswa'))
        except Exception as e:
            db.session.rollback()
            return "Error: {}".format(e), 500

    return render_template('update.html', params=params, post=post)










if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000)

