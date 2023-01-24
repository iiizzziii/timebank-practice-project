# Subor na handlovanie databazy urcenej pre testing
import mysql.connector

# Adresa databazy a aj prihlasovacie udaje do nej
mydb = mysql.connector.connect(
       host="157.245.27.101",
       port='33306',
       user="automation",
       password="ue1roo0uawechai5nieg1B",
       database="timebank_testing",
)

mycursor = mydb.cursor()

# Dropnutie tabuliek
sql1 = "DROP TABLE IF EXISTS Serviceregister, Service, User"

mycursor.execute(sql1)

# Vytvorenie tabulky user
sql2 = "CREATE TABLE User" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "phone VARCHAR(30) NOT NULL," \
       "password VARCHAR(200) NOT NULL," \
       "user_name VARCHAR(30) NOT NULL," \
       "time_account INT NOT NULL," \
       "UNIQUE (phone));"

mycursor.execute(sql2)

# Vytvorenie tabulky service
sql3 = "CREATE TABLE Service" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "title VARCHAR(1000) NOT NULL," \
       "user_id INT NOT NULL," \
       "CONSTRAINT `fk_service_user`FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE ON UPDATE RESTRICT," \
       "estimate INT," \
       "avg_rating INT);"

mycursor.execute(sql3)

# Vytvorenie tabulky serviceregister
sql4 = "CREATE TABLE Serviceregister" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "service_id INT NOT NULL," \
       "CONSTRAINT `fk_serviceregister_service`FOREIGN KEY (service_id)" \
       "REFERENCES Service (id) ON DELETE CASCADE ON UPDATE RESTRICT," \
       "consumer_id INT NOT NULL," \
       "CONSTRAINT `fk_serviceregister_consumer`FOREIGN KEY (consumer_id)" \
       "REFERENCES User (id) ON DELETE CASCADE ON UPDATE RESTRICT," \
       "hours INT," \
       "service_status ENUM ('inprogress','ended') NOT NULL," \
       "end_time DATE," \
       "rating INT);"

mycursor.execute(sql4)
