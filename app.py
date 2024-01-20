import sqlite3
from flask import Flask, request, render_template,g,redirect,url_for

self = sqlite3.connect('split.db',check_same_thread=False)
cursor = self.cursor()
query = 'CREATE TABLE IF NOT EXISTS GROUPS (GROUP_NAME CHAR(60),NUMBER INT, MEMBERS TEXT NOT NULL);'
cursor.execute(query)
query = 'CREATE TABLE IF NOT EXISTS FRIENDS (NAME CHAR(60),AMT_OWED REAL);'
cursor.execute(query)
query = 'CREATE TABLE IF NOT EXISTS USER (NAME CHAR(60),EMAIL CHAR(40),PASSWORD CHAR(20), TOTAL_OWED INT);'
cursor.execute(query)
app = Flask(__name__)

app.static_folder = '.'
app.template_folder='.'
@app.route('/')

def reg():
    return render_template('reg.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cursor.execute('INSERT INTO USER VALUES(?,?,?,?)',(name,email,password,0))
   # cursor.execute('INSERT INTO FRIENDS VALUES(?,?)',(name,0))
    query = 'SELECT * FROM USER;'
    cursor.execute(query)
    result=cursor.fetchall()
    print(result)
    for i in result:
      name2=i[0]
      email2=i[1]
      password=i[2]
    return render_template('account.html',name=name2,email=email2,pw=password)

@app.route('/tohome',methods=['POST'])
def tohome():
    return render_template('home.html')



@app.route('/friends')
def friends():
    query = 'SELECT * FROM FRIENDS;'
    cursor.execute(query)
    result=cursor.fetchall()
    query = 'SELECT TOTAL_OWED FROM USER;'
    cursor.execute(query)
    totals=cursor.fetchall()
    total=0
    for i in totals:
                if i!='[':
                    for j in i:
                        total=int(j)
    return render_template('friends.html',result=result,total=total)

@app.route('/addgroup',methods=['POST'])
def addgroup():
    column1 = request.form['column1']
    column2 = request.form['column2']
    column3 = request.form['column3']
    str1=""
    count=0
    for k in column3.split(","):
        print(k)
        k=k.replace(" ","")
        cursor.execute('SELECT EXISTS(SELECT * FROM FRIENDS WHERE NAME=?)',[k])
        result=cursor.fetchall()
        exists=0
        for i in result:
            if i!='[':
                for j in i:
                    exists=int(j)
        if exists==1:
            str1=str1+k
            str1=str1+", "
            count=count+1
        else:
            continue
    cursor.execute('SELECT EXISTS(SELECT * FROM GROUPS WHERE GROUP_NAME=?)',[column1])
    result=cursor.fetchall()
    exists=0
    for i in result:
        if i!='[':
            for j in i:
                exists=int(j)
            #print(exists)
    query = 'SELECT TOTAL_OWED FROM USER;'
    cursor.execute(query)
    totals=cursor.fetchall()
    total=0
    for i in totals:
                if i!='[':
                    for j in i:
                        total=int(j)
    if exists==0:   
        cursor.execute("INSERT INTO GROUPS VALUES (?,?,?)",(column1,count,str1))
        query = 'SELECT * FROM GROUPS;'
        cursor.execute(query)
        result=cursor.fetchall()
        cursor.execute('SELECT * FROM GROUPS;')
        friends=cursor.fetchall()
        return render_template('groups.html',result=result,friends=friends,total=total)
    else:
        query = 'SELECT * FROM GROUPS;'
        cursor.execute(query)
        result=cursor.fetchall()
        cursor.execute('SELECT * FROM GROUPS;')
        friends=cursor.fetchall()
        return render_template('groups.html',result=result,friends=friends,total=total)

@app.route('/addfriend',methods=['POST'])
def addfriend():
    column1 = request.form['column1']
    cursor.execute('SELECT EXISTS(SELECT * FROM FRIENDS WHERE NAME=?)',[column1])
    result=cursor.fetchall()
    exists=0
    for i in result:
        if i!='[':
            for j in i:
                exists=int(j)
            #print(exists)
    query = 'SELECT TOTAL_OWED FROM USER;'
    cursor.execute(query)
    totals=cursor.fetchall()
    total=0
    for i in totals:
                if i!='[':
                    for j in i:
                        total=int(j)

    if exists==0:    
        cursor.execute("INSERT INTO FRIENDS VALUES (?,?)",(column1,"0"))
        query = 'SELECT * FROM FRIENDS;'
        cursor.execute(query)
        result=cursor.fetchall()
        return render_template('friends.html',result=result,total=total)
    else:
        query = 'SELECT * FROM FRIENDS;'
        cursor.execute(query)
        result=cursor.fetchall()
        return render_template('friends.html',result=result,total=total)



@app.route('/groups')
def groups():
    query = 'SELECT * FROM GROUPS;'
    cursor.execute(query)
    result=cursor.fetchall()
    query = 'SELECT TOTAL_OWED FROM USER;'
    cursor.execute(query)
    totals=cursor.fetchall()
    total=0
    for i in totals:
                if i!='[':
                    for j in i:
                        total=int(j)

    return render_template('groups.html',result=result,total=total)

@app.route('/expense')
def expense():
    query = 'SELECT * FROM FRIENDS;'
    cursor.execute(query)
    friends=cursor.fetchall()
    query = 'SELECT * FROM GROUPS;'
    cursor.execute(query)
    groups=cursor.fetchall()
    return render_template('expense.html',groups=groups,friends=friends)
    
@app.route('/account')
def account():
    query = 'SELECT * FROM USER;'
    cursor.execute(query)
    result=cursor.fetchall()
    for i in result:
      name=i[0]
      email=i[1]
      password=i[2]
    return render_template('account.html',name=name,email=email,pw=password)

@app.route('/edit',methods=['POST'])
def edit():
    name = request.form['column1']
    email = request.form['column2']
    pw = request.form['column3']
    print(name,email,pw)
    cursor.execute('UPDATE USER SET NAME=?',([name]))
    cursor.execute('UPDATE USER SET EMAIL=?',([email]))
    cursor.execute('UPDATE USER SET PASSWORD=?',([pw]))
    query = 'SELECT * FROM USER;'
    cursor.execute(query)
    result=cursor.fetchall()
    print(result)
    for i in result:
      name2=i[0]
      email2=i[1]
      password=i[2]
    return render_template('account.html',name=name2,email=email2,pw=password)

@app.route('/signin', methods=['POST'])
def signin():

    name = request.json['desc']
    amount = request.json['amount']
    grp = request.json['group']
    person = request.json['person']
    flag = request.json['flag']
    entries = request.json['entries']
    amount = int(amount)
    if flag == 0:
        if grp != "":
            cursor.execute(
                "SELECT NUMBER FROM GROUPS WHERE GROUP_NAME=?", (grp,))

            numofmembers = cursor.fetchall()

            cursor.execute(
                "SELECT MEMBERS FROM GROUPS WHERE GROUP_NAME=?", (grp,))

            members = cursor.fetchall()

            num = numofmembers[0][0]
            num = int(num)
            num = num+1
            splitval = amount/num
            list_of_members = members[0][0].split(', ')
            list_of_members.pop()

            for name in list_of_members:
                cursor.execute(
                    f"UPDATE FRIENDS SET AMT_OWED = AMT_OWED + {splitval} WHERE NAME=?", (name,))

            
            cursor.execute(
                f"UPDATE USER  SET TOTAL_OWED = TOTAL_OWED +{splitval}")

        if person != "":

            splitval = amount/2
            cursor.execute(
                f"UPDATE FRIENDS SET AMT_OWED = AMT_OWED +{splitval} WHERE NAME=?", (person,))
            cursor.execute(
                f"UPDATE USER SET TOTAL_OWED = TOTAL_OWED +{splitval}")


    else:
        if grp != "":
            cursor.execute(
                "SELECT MEMBERS FROM GROUPS WHERE GROUP_NAME=?", (grp,))
            members = cursor.fetchall()
            list_of_members = members[0][0].split(', ')
            list_of_members.pop()
            list_of_entries = entries.split(',')
            variable=int(list_of_entries[0])
            cursor.execute(
                f"UPDATE USER SET TOTAL_OWED = TOTAL_OWED +{variable}")

            for i in range(1, len(list_of_entries)):
                entry = list_of_entries[i]
                name = list_of_members[i-1]
                cursor.execute(
                    f"UPDATE FRIENDS SET AMT_OWED = AMT_OWED + {entry} WHERE NAME=?", (name,))

        if person != "":
            list_of_entries = entries.split(',')
            entry=list_of_entries[1]
            cursor.execute(f"UPDATE FRIENDS SET AMT_OWED = AMT_OWED +{entry} WHERE NAME=?",(person,))
            
            variable = list_of_entries[0]
            cursor.execute(
                f"UPDATE USER SET TOTAL_OWED = TOTAL_OWED +{variable}")

    query = 'SELECT * FROM FRIENDS;'
    cursor.execute(query)
    friends=cursor.fetchall()
    query = 'SELECT * FROM GROUPS;'
    cursor.execute(query)
    groups=cursor.fetchall()
    return render_template('expense.html',groups=groups,friends=friends)

 

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__': 
    app.run(host='0.0.0.0')