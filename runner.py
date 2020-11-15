from flask import Flask,render_template,request,redirect,url_for,session,flash,Response
from datetime import datetime,timedelta
#from flask_sqlalchemy import SQLAlchemy
import database_management as dm

app=Flask(__name__)
app.secret_key='emiwaybantai'
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.permanent_session_lifetime=timedelta(days=5)
lis=[1,2,3,4,5]


###APP AREA

@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route("/login_page",methods=["POST","GET"])
def login_page():
    if request.method=="POST":
        session.permanent=True
        username=request.form['username']
        password=request.form['password']
        account_type , cond = dm.check_user_login(username,password)
        if cond==True:

            session['username'] = username
            session['password'] = password
            session['account_type'] = account_type
            #print(account_type)
            return redirect(url_for('account_home'))
        else:
            flash(f"<h5><center>either account doesnt exists or password is wrong boi</center></h5>")
            return redirect(url_for('login_page')) 
    else:
        if "username" in session:
            return redirect(url_for("account_home"))
        else:        
            return render_template("login.html")

@app.route("/signup_page/<account>",methods=["POST","GET"])
def signup_page(account='student'):
    if account=='student':
        if request.method=="POST":
            username=request.form['username']
            password=request.form['password']
            branch    =request.form['branch']
            semester  =request.form['semester']

            if dm.signup(username,password,branch,semester)==True:
                session['username']=username
                session['password']=password
                return redirect(url_for('account_home'))
        else:
            if "username" in session:
                return redirect(url_for('account_home'))
            else:      
                return render_template("signup.html")
    if account=='teacher':
        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']
            #print(request.form.getlist('subject'))
            subjects=request.form.getlist('subject')
            
            if dm.teacher_signup(username,password,subjects)==True:
                #print('ohhh yesss')
                session['username']=username
                session['password']=password
                return redirect(url_for('account_home'))
            else:
                return "Something went wrong"    
        else:
            return render_template('teachers_signup.html') 

@app.route("/user")
def account_home():
    if "username" in session:
        user=session['username']
        return  render_template('login_home.html',user=user)   
    else:
        return redirect(url_for("login_page"))

@app.route("/logout")
def logout():
    session.pop("username",None)
    session.pop("password",None)
    session.pop('account_type',None)
    flash(f"<h5><center>You have been successfully logged out</center></h5>")
    return redirect(url_for('login_page'))       

@app.route('/resources/',methods=['GET',"POST"])
@app.route('/resources/<subject>/<int:page_num>',methods=['GET',"POST"])
def resources(page_num=1,subject=None):
    user=session['username']
    courses_enrolled= dm.get_user_subjects(user,session['account_type'])
    if request.method=='POST':
        #print('got_inside')
        link=request.form['link']
        text=request.form['text']
        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")
        
        dm.insert_resource(subject,link,text,current_time)
        #print('inserted_resource')
        return redirect(url_for('resources'))
    else:
        resources=None
        if subject!= None:
            resources = dm.get_resources(subject)
            #print(resources)
        #print(subject)
        return render_template('resources.html',pn=page_num,subject=subject,courses=courses_enrolled, resources=resources)

@app.route('/doubts')
@app.route('/doubts/<subject>',methods=['GET',"POST"])
@app.route('/doubts/<subject>/<int:doubt_id>',methods=['GET',"POST"])

def doubts(subject=None , doubt_id=None):
    user=session['username']
    courses_enrolled= dm.get_user_subjects(user,session['account_type'])
    doubts=None
    comments=None
    cur_doubt=None
    if request.method=='GET':
        if subject is not None:
            doubts= dm.get_questions(subject)
            #print(doubts)
        if doubt_id is not None:
            cur_doubt=dm.get_doubt(doubt_id)
            comments = dm.handle_reply('get_reply',doubt_id)
            print(comments)
            print(cur_doubt)
        return render_template('doubts.html',subject=subject,courses=courses_enrolled,doubts=doubts,doubt_id=doubt_id,account_type=session['account_type'],comments=comments,cur_doubt=cur_doubt)  

    if request.method=='POST':
        user = session['username']
        if doubt_id is None:
            doubt = request.form['doubt']
            now = datetime.now()
            current_time = now.strftime("%D %H:%M:%S")
            dm.insert_doubt(doubt,user,subject,current_time)
            return redirect(url_for('doubts',subject=subject))

        if doubt_id is not None:
            reply = request.form['reply']
            now = datetime.now()
            current_time = now.strftime("%D %H:%M:%S")
            dm.handle_reply('insert_reply' ,doubt_id,reply,user, subject,current_time)
            return redirect(url_for('doubts',subject=subject,doubt_id=doubt_id))
        
###################################################################################################################     
if __name__=="__main__":
    #database.create_all()
    app.run(debug=True)    
