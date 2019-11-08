from flask import *  

app = Flask(__name__)

def connect():
    import mysql.connector
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="AthlonY2",
    db='railway'
    ) 
    return mydb

#FrontEnd Code

@app.route("/")
def home():
    return render_template("main.html")

@app.route("/book")
def book():
    return render_template("book.html")

@app.route("/view")
def view():
    return render_template("view.html")

@app.route("/delete")
def delete():
    return render_template("delete.html")

#BackEnd Code    

def book_tic(data_dic):
    db=connect()
    cursor=db.cursor(buffered=True)
    cursor.execute("select count(*) from trains where train=\'"+data_dic['train']+" \' and name=\'"+data_dic['name']+'\'')
    f=cursor.fetchone()[0]
    if f is None:
    	f=0
    print(f)
    if f!=0:
        cursor.execute("update trains set seats=seats +"+str(data_dic['seats'])+" where train=\'"+data_dic['train']+"\' and name=\'"+data_dic['name']+'\'')
    else:
        cursor.execute("insert into trains values(NULL,'"+data_dic['train']+"','"+data_dic['name']+"','"+data_dic['seats']+"')")
    db.commit()

def delete_tic(data_dic,arg):
    db=connect()
    cursor=db.cursor()
    if arg=="delrow":
    	print "please delete"
        cursor.execute("delete from trains where train=\'"+data_dic['train']+" \' and name=\'"+data_dic['name']+'\'')
        #cursor.execute("delete from trains where train=\'"+data_dic['train']+" \' and name=\'"+data_dic['name']+'\'')
    else:
        cursor.execute("update trains set seats=seats -"+str(data_dic['seats'])+" where train=\'"+data_dic['train']+"\' and name=\'"+data_dic['name']+'\'')
    db.commit()
    
@app.route('/book_ticket', methods = ['POST'])
def book_ticket():
    data = request.form['canvas_data']
    data_dic = json.loads(data)
    print(data_dic)
    db=connect()
    cursor=db.cursor()
    cursor.execute("select sum(seats) from trains where train= \'"+data_dic['train']+'\'')
    fetch_data=cursor.fetchone()
    if fetch_data==None:
        x=0
    else:
        x=fetch_data[0]
    print x
    if x==None:
    	x=0    
    if x==100:
        return jsonify({'results':'No Tickets available for this train'})
    elif x+int(data_dic['seats'])>100:
        book_tic({'name':data_dic['name'],'train':data_dic['train'],'seats': str(100-x)})
        return jsonify({'results':str(100-x)+' Tickets were succesfully booked'})
    else:
        book_tic(data_dic)
        return jsonify({'results':'Your Tickets were succesfully booked'})

@app.route('/delete_ticket',methods=['POST'])
def delete_ticket():
    data = request.form['canvas_data']
    data_dic = json.loads(data)
    print(data_dic)
    db=connect()
    cursor=db.cursor()
    cursor.execute("select seats from trains where train=\'"+data_dic['train']+" \' and name=\'"+data_dic['name']+'\'')
    #cursor.execute("select seats from trains where name=\'"+data_dic['name']+'\''+"and train=\' "+data_dic['train']+'\'')
    #cursor.execute("select seats from trains where name='hello' and train='Y'")
    print("select seats from trains where name=\'"+data_dic['name']+'\''+"and train=\'"+data_dic['train']+'\'')
    fetch_data=cursor.fetchone()
    print(fetch_data)
    if fetch_data==None:
        x=0
    else:
        x=fetch_data[0]
    print x
    if x==0:
        return jsonify({'results':'You have no booked tickets in this train'})
    elif x>int(data_dic['seats']):
        delete_tic(data_dic,arg="updrow")
        return jsonify({'results':str(data_dic['seats'])+' of your tickets were deleted'})
    else:
    	delete_tic(data_dic,arg="delrow")
        return jsonify({'results':'All your tickets were deleted'})
               
@app.route('/view_trains',methods=['GET'])
def display_table():
    db=connect()
    cursor=db.cursor()
    avail={}
    cap={}
    cursor.execute("select train,maxcap from train_names")
    res=cursor.fetchall()
    trains=[]
    for i in range(cursor.rowcount):
        avail[res[i][0]]=res[i][1]
        cap[res[i][0]]=str(res[i][1])
        trains.append(str(res[i][0]))
    cursor.execute("select train,sum(seats) from trains group by train ")
    res=cursor.fetchall()
    print cursor.rowcount
 
    
    updated=[]
    for i in range(cursor.rowcount):
        avail[res[i][0]]=str(avail[res[i][0]]-(res[i][1]))
        updated.append(res[i][0])
    for i in trains:
    	if i not in updated:
    		avail[i]=cap[i]
 
    print(avail)
    return jsonify(avail)
    

if __name__ == "__main__":
    app.run(debug=True)