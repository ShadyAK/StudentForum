import sqlite3

connection = sqlite3.connect("social media/temp.db")
cur = connection.cursor()

sql_command = """CREATE TABLE IF NOT EXISTS student_details (  
username VARCHAR(13) PRIMARY KEY,  
password VARCHAR2(50),  
branch VARCHAR(30),  
semester INTEGER(1));"""

cur.execute(sql_command)
connection.commit()
#cur.execute('INSERT INTO student_details VALUES(?,?,?,?)',('0801CS181018','Ashwin7#','C.S.E.',5))
#connection.commit()
'''cur.execute('SELECT username FROM student_details WHERE username=(?) AND password=(?)',('0801CS181018','Ashwin70#'))
result=cur.fetchone()
print(result)
if result:
    print(type(result[0]))'''
'''
subjects="""
CREATE TABLE IF NOT EXISTS subjects(
    _id VARCHAR(10) PRIMARY KEY,
    branch VARCHAR(10) NOT NULL,
    semester INT(1) NOT NULL
)
"""
cur.execute(subjects)
SQLs=["""INSERT INTO subjects VALUES('DBMS','C.S.E',5)""",
      """INSERT INTO subjects VALUES('TOC','C.S.E',5) """,
      """INSERT INTO subjects VALUES('Physics','Civil',2)""",
      """INSERT INTO subjects VALUES('M.L','I.T',7)"""]
for SQL in SQLs:
    print(SQL)
    cur.execute(SQL)
connection.commit()    '''

teachers='''CREATE TABLE IF NOT EXISTS teacher(
    username PRIMARY KEY NOT NULL,
    password NOT NULL
)
'''
cur.execute(teachers)
connection.commit()
resources="""CREATE TABLE IF NOT EXISTS resources(
          subject_id TEXT,
          link VARCHAR2(200),
          description VARCHAR2(400),
          time_posted timestamp,
          FOREIGN KEY(subject_id) REFERENCES subjects(_id))"""
cur.execute(resources)
connection.commit()

temp="SELECT MAX(rowid) FROM subjects"
cur.execute(temp)
print(cur.fetchone()[0])


teaches="""CREATE TABLE IF NOT EXISTS teaches(
             
             username TEXT NOT NULL,
             subject_id TEXT,
             FOREIGN KEY(subject_id) REFERENCES subjects(_id)
             FOREIGN KEY(username) REFERENCES teacher(username)   
)"""
cur.execute(teaches)
connection.commit()

doubts="""CREATE TABLE IF NOT EXISTS discussion(
             
             doubt_id INTEGER PRIMARY KEY AUTOINCREMENT,
             doubt TEXT ,
             asked_by TEXT ,
             subject_id TEXT,
             time_posted timestamp,
             FOREIGN KEY(asked_by) REFERENCES student_details(username),
             FOREIGN KEY(subject_id) REFERENCES subjects(_id)
               
)"""

cur.execute(doubts)
connection.commit()

reply="""CREATE TABLE IF NOT EXISTS reply(
             
             reply_id INTEGER PRIMARY KEY AUTOINCREMENT,
             reply TEXT ,
             reply_by TEXT ,
             subject_id TEXT,
             doubt_id INTEGER,
             time_posted timestamp,
             FOREIGN KEY(reply_by) REFERENCES student_details(username),
             FOREIGN KEY(subject_id) REFERENCES subjects(_id),
             FOREIGN KEY(doubt_id) REFERENCES discussion(doubt_id)
               
)"""

cur.execute(reply)
connection.commit()

like_doubt ="""CREATE TABLE IF NOT EXISTS like_doubt(
             
             doubt_id INTEGER ,
             liker_id TEXT ,

             FOREIGN KEY(doubt_id) REFERENCES discussion(doubt_id),
             FOREIGN KEY(liker_id) REFERENCES student_details(usename)
             ON DELETE CASCADE  
)"""

cur.execute(like_doubt)
connection.commit()

like_reply = """CREATE TABLE IF NOT EXISTS like_reply(
             
             reply_id INTEGER ,
             liker_id TEXT ,

             FOREIGN KEY(reply_id) REFERENCES reply(reply_id),
             FOREIGN KEY(liker_id) REFERENCES student_details(usename)
             ON DELETE CASCADE  
)"""

cur.execute(like_reply)
connection.commit()