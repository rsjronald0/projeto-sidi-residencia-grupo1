import json
from flask import Flask, request
import mysql.connector

app = Flask(__name__)
db_exists = False
vagas_exists = False
perguntas_exists = False
respostas_exists = False

mydb = mysql.connector.connect(
  host="localhost",
  user="sidi",
  password="sidi"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

for m in mycursor:
    for v in m:
        if (v == 'gupy_service'):
            db_exists = True

if (db_exists == False):
  mycursor.execute("CREATE DATABASE gupy_service")

mydb = mysql.connector.connect(
  host="localhost",
  user="sidi",
  password="sidi",
  database="gupy_service"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

t = ''
for t in mycursor:
  for v in t:
    if (v == 'vagas'):
        vagas_exists = True
    if (v == 'perguntas'):
        perguntas_exists = True
    if (v == 'respostas'):
        respostas_exists = True

if (vagas_exists == False):
  mycursor.execute("CREATE TABLE vagas (id_vaga INT PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT, nome VARCHAR(200))")

if (perguntas_exists == False):
  mycursor.execute("CREATE TABLE perguntas (id_pergunta INT PRIMARY KEY UNIQUE AUTO_INCREMENT, id_vaga INT NOT NULL, pergunta VARCHAR(350), tipo ENUM('obrigatoria', 'eliminatoria'), FOREIGN KEY (id_vaga) REFERENCES vagas(id_vaga))")

if (respostas_exists == False):
  mycursor.execute("CREATE TABLE respostas (id_usuario INT NOT NULL, id_vaga INT NOT NULL, id_pergunta INT NOT NULL, resposta VARCHAR(350), FOREIGN KEY (id_vaga) REFERENCES vagas(id_vaga), FOREIGN KEY (id_pergunta) REFERENCES perguntas(id_pergunta))")

@app.route("/check/<job_id>", methods=["GET"])
def check_job_id(job_id):
    sql = "SELECT id_vaga FROM vagas WHERE id_vaga = %s"
    job = (job_id,)
    mycursor.execute(sql, job)
    myresult = mycursor.fetchall()
    if (len(myresult) < 1):
       return 'False'
    else:
       return 'True'

@app.route("/job_messages/<user_id>", methods=["GET"])
def get_job_messages(user_id):
    sql = "SELECT id_usuario, r.id_vaga, pergunta, resposta, tipo FROM respostas r JOIN perguntas p ON r.id_pergunta = p.id_pergunta WHERE id_usuario = %s"
    user = (user_id,)
    mycursor.execute(sql, user)
    myresult = mycursor.fetchall()
    if (len(myresult) < 1):
       return False
    else:
        myarray = []
        for m in myresult:
           mydict = ([{
              "id_usuario": myresult[myresult.index(m)][0],
              "id_vaga": myresult[myresult.index(m)][1],
              "pergunta": myresult[myresult.index(m)][2],
              "resposta": myresult[myresult.index(m)][3],
              "tipo": myresult[myresult.index(m)][4],
           }])
           myarray.append(mydict)
        dictresp = {
           "resp": myarray
        }
        return dictresp

@app.route("/job_application", methods=["POST"])
def job_application():
    application = json.loads(request.data)

    user_id = 1
    respostas = []
    count = 1

    users = "SELECT max(id_usuario) FROM respostas"
    mycursor.execute(users)
    myresult = mycursor.fetchall()
    if (myresult[0][0] is not None):
       user_id = myresult[0][0] + 1

    for a in application:
      if (a == 'id_vaga' or a == 'vaga'):
        vaga = application[a]
      else:
        respostas.append(application[a])
    
    for r in respostas:
       sql = "INSERT INTO respostas(id_usuario, id_vaga, id_pergunta, resposta) VALUES (%s, %s, %s, %s)"
       data = (user_id, vaga, count, r)
       mycursor.execute(sql, data)
       mydb.commit()
       count += 1

    return "Respostas inseridas com sucesso"

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)