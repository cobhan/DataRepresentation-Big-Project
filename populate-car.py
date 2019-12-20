import mysql.connector
import dbconfig as cfg

db = mysql.connector.connect(
  host=cfg.mysql['host'],
  user=cfg.mysql['user'],
  password=cfg.mysql['password'],
  database=cfg.mysql['database']
)

cursor = db.cursor()


sql='insert into car (make, model, price) values (%s,%s,%s)'
values=("Subaru","Impreza",50000)

cursor.execute(sql, values)

db.commit()
print("1 record inserted, ID:", cursor.lastrowid)

