def connect():
    import mysql.connector
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="AthlonY2",
    db='railway'
    ) 
    return mydb

mydb=connect()
cursor=mydb.cursor()
cr_db="create db railway"
#sql="create table trains(id int AUTO_INCREMENT primary key,train varchar(10),name varchar(20),seats int)"
#cursor.execute(sql)
#="insert into trains values(2,'x','sxxhus',20)"
#cursor.execute(sql)
#sql="create table train_names(id int AUTO_INCREMENT primary key,train varchar(10),maxcap int)"
#cursor.execute(sql)
#cursor.execute("insert into train_names values(NULL,'X',100)")
#cursor.execute("insert into train_names values(NULL,'Y',100)")
#cursor.execute("insert into train_names values(NULL,'Z',100)")
mydb.commit()
cursor.execute("delete from trains")
mydb.commit()
