import mysql.connector
import dbconfig as cfg

db = mysql.connector.connect(
  host=cfg.mysql['host'],
  user=cfg.mysql['user'],
  password=cfg.mysql['password'],
  database=cfg.mysql['database']
)

cursor = db.cursor()
sql="CREATE TABLE accessories (id INT AUTO_INCREMENT PRIMARY KEY, type VARCHAR(255), brand VARCHAR(255), price INT)"

cursor.execute(sql)

#could not get 2 databases working so replaced accessories with a quick img gallery




