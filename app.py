from flask import Flask ,render_template,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_ckeditor import CKEditor, CKEditorField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


app = Flask(__name__)
ckeditor = CKEditor(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' 

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:marty1234@localhost/blogs_data' 



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
db = SQLAlchemy(app)



# class Todo(db.Model):
#     Sno = db.Column(db.Integer, primary_key = True) 
#     title = db.Column(db.String(200), nullable = False)
#     Desc = db.Column(db.text) 
#     # Desc = db.Column(CKEditorField(validators=[DataRequired()]), nullable=False)
#     Date_created = db.Column(db.DateTime, default= datetime.utcnow())


    # Desc = db.Column(CKEditorField(validators=[DataRequired()]), nullable=False)
    # blog_img = db.C 


# class source_code(db.Model):
#     Sno = db.Column(db.Integer, primary_key = True) 
#     title = db.Column(db.String(200), nullable = False) 
#     Desc = db.Column(db.String(500), nullable = False) 
#     # Desc = db.Column(CKEditorField(validators=[DataRequired()]), nullable=False)
#     Date_created = db.Column(db.DateTime, default= datetime.utcnow()) 


class POSTS(db.Model):
    Sno = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(200), nullable = False) 
    # author = db.Column(db.String(200), nullable = False) 
    Desc = db.Column(db.Text) 
    Date_created = db.Column(db.DateTime, default= datetime.utcnow())

    def __repr__(self):
            return f"{self.Sno} - {self.title}"
with app.app_context():
    db.create_all()
    

@app.route("/blogs")
def blog():
    post = POSTS.query.all()
    return render_template('blog.html', allposts = post) 

@app.route("/")
def home():
    return render_template('index.html') 

@app.route("/source_code", methods = ['GET', 'POST'])
def add_sourcecode():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['title']
        desc = request.form['desc']
        post = POSTS(title = title , Desc = desc)
        db.session.add(post)
        db.session.commit()

    redirect('source_code.html')   
    allposts = POSTS.query.all()
    return render_template('source_code.html', allposts = allposts)


@app.route("/dashboard", methods = ['GET', 'POST']) 
def dashboard():
    if request.method == 'POST': 
        title = request.form['title']
        desc = request.form['desc']
        post = POSTS(title = title, Desc = desc)
        db.session.add(post)
        db.session.commit()
        redirect('dashboard.html')
    allposts = POSTS.query.all()
    return render_template('dashboard.html', allposts = allposts) 


@app.route("/update/<int:sno>", methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        post = POSTS.query.filter_by(Sno=sno).first() 
        post.title = title
        post.Desc = desc
        db.session.add(post)
        db.session.commit()
        return redirect('/dashboard')
    
    post = POSTS.query.filter_by(Sno=sno).first() 
    return render_template('update.html', post=post)
   

@app.route("/delete/<int:sno>")
def delete(sno):
    post = POSTS.query.filter_by(Sno=sno).first()
    db.session.delete(post)
    db.session.commit()
    return redirect('/dashboard')

@app.route("/show_blog/<int:sno>")
def blog_page(sno):
    post = POSTS.query.filter_by(Sno=sno).first()
    return render_template('blogs_page.html' , post=post)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__" :
    app.run(debug=True , port=8000)