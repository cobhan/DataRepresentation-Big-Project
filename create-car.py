import mysql.connector
import dbconfig as cfg

db = mysql.connector.connect(
  host=cfg.mysql['host'],
  user=cfg.mysql['user'],
  password=cfg.mysql['password'],
  database=cfg.mysql['database']
)

cursor = db.cursor()
sql="CREATE TABLE car (id INT AUTO_INCREMENT PRIMARY KEY, make VARCHAR(255), model VARCHAR(255), price INT)"

cursor.execute(sql)





