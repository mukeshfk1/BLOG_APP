from flask import Flask
from flask import render_template,redirect,url_for,request
import models
import utils
from sqlalchemy.orm import joinedload,load_only
from datetime import datetime
from database import create_tables,create_session
from flask_login import LoginManager,current_user,login_required,login_user,logout_user
           
                        


app = Flask(__name__)
app.config['SECRET_KEY']='decr5f567yggyh'

login = LoginManager()


login.init_app(app)



@login.user_loader
def load_user(user_id, db = create_session()):
    user = db.query(models.User).get(user_id)
    db.close()
    return user 
8

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup/', methods=['POST'])
def signup(db = create_session()):

    form_name = request.form['name']
    form_gender = request.form['gender']
    form_email = request.form['email']
    
    form_password = request.form['password']
    
    new_user = models.User()
    
    new_user.name = form_name
    new_user.username = form_email
    new_user.email = form_email
    new_user.password = utils.hash_password(form_password)
    new_user.gender = form_gender
    new_user.created_at = datetime.now()

    try:
        db.add(new_user)
        db.commit()
        db.close()
        
    except:
        db.rollback()
        db.close()
        return {'detail':f'{form_email} already exists'}
        
    return redirect(url_for('home'))

@app.route("/login/", methods=["POST"])
def user_login(db=create_session()):

    form_email = request.form['email']
    form_password = request.form['password']

    db_user = db.query(models.User).filter(models.User.email == form_email).first()
    


    #this is when user does not exists in database.
    if db_user == None:
        db.close()
        return {'detail':f'{form_email} is not exists.'}
    
    verify = utils.verify_password(db_user.password,form_password) 
    
    db.close()
    if verify:
       
        login_user(db_user)
        return redirect ('/view/')
    else:
        return {'details': "wrong password"}

@app.route('/view/')
@login_required
def homepage(db= create_session()):
    db_blogs = db.query(models.Blogs).options(joinedload(models.Blogs.user_blog).load_only('name','email')).filter(models.Blogs.is_deleted == 0).all()
    db.close()
    

    return render_template('view.html',user = current_user, data = db_blogs)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route("/newblog/", methods = ["POST"])
@login_required
def new_blog(db=create_session()):

    form_title = request.form['title']
    form_content = request.form['content']

    new_blog = models.Blogs()
    
    new_blog.author=current_user.id
    new_blog.content= form_content
    new_blog.title=form_title
    new_blog.created_at=datetime.now()
    new_blog.is_deleted = 0

    try:
        db.add(new_blog)
        db.commit()
        db.close()

    except:
        db.rollback()
        db.close()
    
    return redirect('/view/')


@app.route('/like/<blog_id>', methods = ["GET"])
@login_required
def blog_like(blog_id,db = create_session()):

    db_likes = db.query(models.Likes).filter((models.Likes.user_id == current_user.id),(models.Likes.blog_id == blog_id)).first()

    if db_likes != None:
        db.delete(db_likes)

    else:
        new_like = models.Likes()

        new_like.blog_id = blog_id
        new_like.user_id = current_user.id 
        new_like.created_at = datetime.now()

        db.add(new_like)
    db.commit()
    db.close()    

    return redirect('/view/')

@app.route('/editblog/<blog_id>', methods = ['POST'])
@login_required
def update_blog(blog_id,db = create_session()):

    db_blog = db.query(models.Blogs).filter((models.Blogs.id == blog_id),(models.Blogs.author == current_user.id)).first()

    if db_blog == None:
        db.close()
        return {'details': 'Unauthorized attempt'}
    
    db_blog.title = request.form.get('title')
    db_blog.content = request.form.get('content')

    db.commit()
    db.close()

    return redirect('/view/')
    




        




if __name__ == "__main__":
    create_tables()
    app.run(debug=True)