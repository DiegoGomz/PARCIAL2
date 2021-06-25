from flask import render_template, flash, redirect, url_for
from app import app
from app import Bootstrap
from app import db
from app.forms import LoginForm, NotasForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Notas
import uuid

@app.route("/")
@app.route("/index")
def index():
    

    if not current_user.is_authenticated:
        return redirect(url_for("login",id=uuid.uuid4()))
    o=""
    Lista=Notas.query.filter_by(users_id=current_user.id).all()
    return render_template("index.html", lista=Lista)



@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Credenciales no validas. Favor de ingresar credenciales validas.")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("¡Inicio de sesión exitoso! {}".format(form.username.data))
        return redirect(url_for("index",id=uuid.uuid4()))
    return render_template("login.html", title="Login",form=form)


@app.route("/Fallo")
@login_required
def secreto():
    return "Fallo"

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index",id=uuid.uuid4()))


@app.route("/appnotas/delete/<int:id>", methods=["POST"])
@login_required
def delete_contact(id):
    appnotas= Notas.query.filter_by(id=id).first()
    if appnotas:
        if current_user.id==appnotas.users_id:
            db.session.delete(appnotas)
            db.session.commit()
            return redirect(url_for("index",id=uuid.uuid4()))
        else:
            return redirect(url_for("404"))
    else:
        flash("Esta nota no esta disponible")
    return redirect(url_for("index",id=uuid.uuid4()))

@app.route("/appnotas/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_contact(id):
    appnotas= Notas.query.filter_by(id=id).first()
    if appnotas:
        if current_user.id==appnotas.users_id:
            pass
            form=NotasForm()
            if form.validate_on_submit():
                appnotas.name=form.name.data
                appnotas.email=form.email.data
                appnotas.number=form.number.data
                appnotas.users_id=current_user.id
                db.session.add(appnotas)
                db.session.commit()
                return redirect(url_for("index",id=uuid.uuid4()))
            form.name.data=appnotas.name
            form.email.data=appnotas.email
            form.number.data=appnotas.number
            edit=True
            return render_template("appnotas.html", edit=edit,form=form)
        else:
            return redirect(url_for("404"))
    return redirect(url_for("index",id=uuid.uuid4()))

@app.route("/appnotas", methods=["GET", "POST"])
@login_required
def appnotas():
    form=NotasForm()  
    if form.validate_on_submit():
        p=Notas()
       
        p.name=form.name.data
        p.email=form.email.data
        p.number=form.number.data
        p.users_id=current_user.id
        db.session.add(p)
        db.session.commit()
        return redirect(url_for("index",id=uuid.uuid4()))
    return render_template("appnotas.html", form=form, edit=False)

    

@app.route("/signup", methods=["GET", "POST"])
def singup():
    if current_user.is_authenticated:
         return redirect(url_for("index",id=uuid.uuid4()))
    form=SignUpForm()
    if form.validate_on_submit():
        user= User.query.filter_by(username=form.username.data).first()
        if user:
            return redirect(url_for("signup"))
        user= User.query.filter_by(email=form.email.data).first()
        if user:
            return redirect(url_for("signup"))
        u=User()
        u.username=form.username.data
        u.email=form.email.data
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html", form=form)
    

    

    

