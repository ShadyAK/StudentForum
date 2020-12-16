#from runner import account_credentials
import sqlite3
from collections import Counter
connection=sqlite3.connect('social media/temp.db',check_same_thread=False)


def signup(name,password,branch,semester):
    cur=connection.cursor()
    cur.execute("SELECT * FROM student_details WHERE username=(?);",(name,))
    result=cur.fetchone()
    if result is None:
        cur.execute('INSERT INTO student_details VALUES(?,?,?,?);',(name,password,branch,semester))
        connection.commit()
        cur.close()
        return True
    else:
        cur.close()
        return False    

           
def check_user_login(name,password):
    cur=connection.cursor()
    result = cur.execute('SELECT username FROM student_details WHERE username=(?) AND password=(?);',(name,password)).fetchone()
    
    if result:
        cur.close()
        account_type='student'
        return account_type,True
    else:
        result = cur.execute('SELECT username FROM teacher WHERE username=(?) AND password=(?);',(name,password)).fetchone()
        if result:
            account_type='teacher'
            print('teacher')
            cur.close()
            return account_type,True
        
        else:
            cur.close()
            return None,False    
def teacher_signup(name,password,subjects):
    cur = connection.cursor()
    cur.execute("SELECT * FROM teacher WHERE username=(?);",(name,))
    result=cur.fetchone()
    if result is None :
        cur.execute('INSERT INTO teacher VALUES(?,?)',(name,password))
        for subject in subjects:
            cur.execute('INSERT INTO teaches VALUES(?,?)',(name,subject))
        connection.commit()
        return True
    else:
        return False                 

def insert_resource(course,link,des,time):
    cur=connection.cursor()
    cur.execute("INSERT INTO resources VALUES(?,?,?,?)",(course,link,des,time))
    cur.close()
    connection.commit()
    print('resource added')

def get_db_len(name):
    sql='SELECT MAX(rowid) FROM '+name
    cur=connection.cursor()
    cur.execute(sql)
    result=cur.fetchone()[0]
    return result 

def get_user_subjects(name,account_type):
    cur=connection.cursor()
    if account_type=='student':
        cur.execute('SELECT _id FROM student_details JOIN subjects ON student_details.branch=subjects.branch AND student_details.semester = subjects.semester WHERE username=(?);',(name,))
        result=cur.fetchall()
    else:
        cur.execute('SELECt subject_id FROM teaches WHERE username=(?)',(name,))
        result=cur.fetchall()    
    return result   


def get_resources(sub):
    cur=connection.cursor()
    cur.execute("SELECT link , description FROM RESOURCES WHERE subject_id=(?)",(sub,)) 
    result=cur.fetchall()
    return result   

def get_questions(sub):
    cur = connection.cursor()
    cur.execute("SELECT doubt_id , doubt FROM discussion WHERE subject_id=(?)",(sub,))
    result= cur.fetchall()
    return result

def insert_doubt(doubt,asked_by,sub,time):
    cur = connection.cursor()
    cur.execute("INSERT INTO discussion(doubt,asked_by,subject_id,time_posted) VALUES(?,?,?,?)",(doubt,asked_by,sub,time))
    connection.commit()

def handle_reply(task ,doubt_id, reply=None ,reply_by=None,subject=None,time=None):
    cur = connection.cursor()
    if task=='insert_reply':
        cur.execute("""INSERT INTO reply(reply,reply_by,subject_id,doubt_id,time_posted) 
        VALUES(?,?,?,?,?)""",(reply,reply_by,subject,doubt_id,time))
        connection.commit()
    if task == 'get_reply':
        cur.execute('SELECT reply,reply_id FROM reply WHERE doubt_id=(?)',(doubt_id,))    
        result = cur.fetchall()
        return result
def get_doubt(doubt_id):
    cur = connection.cursor()
    cur.execute('SELECT doubt FROM discussion WHERE doubt_id=(?)',(doubt_id,))
    result = cur.fetchone()
    return result         
                
def check_upvote(username,doubt_id):
    cur = connection.cursor()
    cur.execute('SELECT * FROM like_doubt WHERE doubt_id=(?) AND liker_id=(?)',(doubt_id,username))
    result = cur.fetchone()
    if result is None:
        return False
    else:
        return True                    

def upvote_doubt(username,doubt_id):
    cur = connection.cursor()
    cur.execute('INSERT INTO like_doubt VALUES(?,?)',(doubt_id,username))
    connection.commit()
    return True
    
def like_comment(username,reply_id):
    cur = connection.cursor()
    cur.execute('INSERT INTO like_reply VALUES(?,?)',(reply_id,username))
    connection.commit()

def comment_like_status(username,comments):    
    cur = connection.cursor()
    like_status = []
    for comment in comments:
        cur.execute("SELECT * FROM like_reply WHERE liker_id=(?) and reply_id=(?)",(username,comment[1]))
        result = cur.fetchone()
        if result:
            like_status.append(1)
        else:
            like_status.append(0)
    return like_status             

def get_student_contributions(branch=None,semester=None):
    cur = connection.cursor()
    cur.execute('SELECT asked_by,count(*) FROM like_doubt LEFT JOIN discussion ON like_doubt.doubt_id = discussion.doubt_id LEFT JOIN student_details ON discussion.asked_by=student_details.username GROUP BY asked_by HAVING (branch=(?) and semester=(?)) ;',(branch,semester))    
    result1=Counter(dict(cur.fetchall()))
    cur.execute('SELECT reply_by,count(*) FROM like_reply LEFT JOIN reply ON like_reply.reply_id = reply.reply_id LEFT JOIN student_details ON reply.reply_by=student_details.username GROUP BY reply_by HAVING(branch=(?) and semester=(?));',(branch,semester))    
    result2=Counter(dict(cur.fetchall()))
    result = result1+result2
    return result
