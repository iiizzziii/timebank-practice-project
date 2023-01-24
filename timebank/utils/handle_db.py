# Subor na handlovanie testovacej a produkcnej databazy
import mysql.connector

mydb = mysql.connector.connect(
       # host="127.0.0.1",  # Localhost
       host="157.245.27.101",  # Testing
       # host="157.230.79.85",  # Production
       port='33306',
       user="automation",
       password="ue1roo0uawechai5nieg1B",  # Testing
       # password="Fej1chahgheebohxohxi",  # Production
       database="timebank",
)

mycursor = mydb.cursor()

sql1 = "DROP TABLE IF EXISTS Serviceregister, Service, User"

mycursor.execute(sql1)

sql2 = "CREATE TABLE User" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "phone VARCHAR(30) NOT NULL," \
       "password VARCHAR(200) NOT NULL," \
       "user_name VARCHAR(30) NOT NULL," \
       "time_account INT NOT NULL," \
       "UNIQUE (phone));"

mycursor.execute(sql2)

sql3 = "CREATE TABLE Service" \
       "(id INT PRIMARY KEY AUTO_INCREMENT," \
       "title VARCHAR(1000) NOT NULL," \
       "user_id INT NOT NULL," \
       "CONSTRAINT `fk_service_user`FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE ON UPDATE RESTRICT," \
       "estimate INT," \
       "avg_rating INT);"

mycursor.execute(sql3)

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

sql11 = "INSERT INTO User (phone, user_name, time_account, password)" \
       "VALUES ('+421 905 111222', 'Obi-wan Kenobi', '0', 'pbkdf2:sha256:" \
       "260000$qUuINo35hAjbk5Dj$3ceb9922280ebf310a0a85b07166b567c3a03be3d2e36e6de518f9bdd3cf17e8');"

sql12 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 333444', 'Darth Vader', '2', 'pbkdf2:sha256:" \
       "260000$3cJodGWIgbIjR8iI$3b47d9e57d8623ffb38f6131814e716fcf76fd86d2b69607ac78c0ba0ec32eb1');"

sql13 = "INSERT INTO User (phone, user_name, time_account, password)"\
       "VALUES ('+421 905 555666', 'Qui-gon Jinn', '0', 'pbkdf2:sha256:" \
       "260000$W6LTjHepYIohlpC0$909ea33caf04ce34215c23a1ed39b4088c699b0979a7c9e46d27063df3d6a237');"

sql21 = "INSERT INTO Service (title, user_id, estimate, avg_rating)" \
       "VALUES ('Pokosim travnik s motorovou kosackou za polnoci za zvuku vytia vlkov', '1', '2', '0');"

sql22 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Pokosim zahradu', '2');"

sql23 = "INSERT INTO Service (title, user_id, estimate)" \
       "VALUES ('Pozehlim pradlo', '3', '1');"

sql24 = "INSERT INTO Service (title, user_id, estimate, avg_rating)" \
       "VALUES ('Vyperiem pradlo', '3', '2', '1');"

sql25 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Postriham kriky', '2');"

sql26 = "INSERT INTO Service (title, user_id)" \
       "VALUES ('Porylujem zahradu', '3');"

sql27 = "INSERT INTO Service (title, user_id, estimate, avg_rating)" \
       "VALUES ('Vymalujem dom', '2', '8', '3');"

sql28 = "INSERT INTO Service (title, user_id, estimate)" \
       "VALUES ('Vynesiem smeti', '1', '1');"

sql29 = "INSERT INTO Service (title, user_id, estimate, avg_rating)" \
       "VALUES ('Vymalujem plot', '1', '4', '4');"

sql31 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('1', '2', 'inprogress');"

sql32 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status, end_time, rating, hours)" \
       "VALUES ('2', '3', 'ended', '2020-05-12', '4', '2');"

sql33 = "INSERT INTO Serviceregister (service_id, consumer_id, service_status)" \
       "VALUES ('3', '1', 'inprogress');"

mycursor.execute(sql11)
mycursor.execute(sql12)
mycursor.execute(sql13)

mycursor.execute(sql21)
mycursor.execute(sql22)
mycursor.execute(sql23)
mycursor.execute(sql24)
mycursor.execute(sql25)
mycursor.execute(sql26)
mycursor.execute(sql27)
mycursor.execute(sql28)
mycursor.execute(sql29)

mycursor.execute(sql31)
mycursor.execute(sql32)
mycursor.execute(sql33)

mydb.commit()
