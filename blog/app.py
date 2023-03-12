from flask import Flask , render_template ,redirect, request , url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)




class Post(db.Model):
    __tablename__ = "post"
    id =db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable = False)
    fecha = db.Column(db.DateTime, default = datetime.now)
    texto = db.Column(db.String, nullable = False)


@app.route("/")
def inicio():
	posts = Post.query.order_by(Post.fecha.desc()).all() 
	return render_template("inicio.html", posts=posts)




@app.route("/agregar")
def agregar():
	return render_template("agregar.html")

@app.route("/crear", methods=["POST"])
def crear_post():
	titulo = request.form.get("titulo")
	texto = request.form.get("texto")
	post = Post(titulo=titulo, texto=texto)
	db.session.add(post)
	db.session.commit()
	return redirect("/")

@app.route("/borrar", methods=["POST"])
def borrar():
	post_id = request.form.get("post_id")
	post = db.session.query(Post).filter(Post.id==post_id).first()
	db.session.delete(post)
	db.session.commit()
	return redirect("/")


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

