from flask import Flask,render_template,request
import sqlite3
import logging

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("timesheet.html")

@app.route("/a")
def home1():
    return "timesheet.html"

@app.route("/b")
def home2():
    return render_template("timesheet1.html")

@app.route("/clock")
def clock():
    create_db()
    clock_data = query_db()
    return render_template("clock.html",clock_data=clock_data)


@app.route("/clocktable")
def clocktable():
    return render_template("clock_table.html")


@app.route("/clock_activity", methods = ['GET','POST'])
def clock_activity():
    if request.method == 'GET':
        return render_template("clock_activity.html")
    else:
        clock_dat = (request.form['WeekName'],request.form['EmpName'],request.form['Desc'])
        print(clock_dat)
        insert_db(clock_dat)
        return 'Here is the POST request'
   
def create_db():
    logging.info("Hello in create_db")
    conn = sqlite3.connect('clock.db')
    c = conn.cursor()
    try:
        c.execute(""" create table clock_details( id integer primary key autoincrement,week_name text ,emp_name text, description text)""")
        c.execute(""" Insert into clock_details (week_name , emp_name, description) values
              ('WK1', 'Thulasi' , 'Please approve'),
              ('WK2','Hemsagar', 'Worked hard'),
              ('WK3','Saanvi','Cool Work')""")
    except Exception as e:
        logging.info("Error  in create_db"+ str(e))
        print("exception",e)
    conn.commit()
    conn.close()

def query_db():
    logging.info("Hello in query_db")
    conn = sqlite3.connect('clock.db')
    c = conn.cursor()
    c.execute(""" select * from  clock_details""")
    clock_det = c.fetchall()
    conn.commit()
    conn.close()
    return clock_det

def insert_db(clock_act):
    logging.info("Hello in query_db")
    conn = sqlite3.connect('clock.db')
    c = conn.cursor()
    sql_qry = " INSERT INTO clock_details (week_name , emp_name, description) values (?,?,?)"
    c.execute(sql_qry,clock_act)
    clock_det = c.fetchall()
    conn.commit()
    conn.close()
    return clock_det

 
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
