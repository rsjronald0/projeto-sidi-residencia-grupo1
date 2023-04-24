import json
from flask import Flask, request
import mysql.connector

app = Flask(__name__)
db_exists = False
vagas_exists = False
perguntas_eliminatorias_exists = False
perguntas_obrigatorias_exists = False

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
    if (v == 'perguntas_eliminatorias'):
        perguntas_eliminatorias_exists = True
    if (v == 'perguntas_obrigatorias'):
        perguntas_obrigatorias_exists = True

if (vagas_exists == False):
  mycursor.execute("CREATE TABLE vagas (id INT PRIMARY KEY, nome VARCHAR(200))")

if (perguntas_obrigatorias_exists == False):
  mycursor.execute("CREATE TABLE perguntas_obrigatorias (id_usuario INT PRIMARY KEY NOT NULL UNIQUE AUTO_INCREMENT, nome VARCHAR(300), email VARCHAR(250), formacao VARCHAR(300), tecnologias VARCHAR(300))")

if (perguntas_eliminatorias_exists == False):
  mycursor.execute("CREATE TABLE perguntas_eliminatorias (id_usuario INT NOT NULL UNIQUE AUTO_INCREMENT, experiencia_area BOOLEAN, ingles BOOLEAN, python BOOLEAN, FOREIGN KEY (id_usuario) REFERENCES perguntas_obrigatorias(id_usuario))")

@app.route("/check/<job_id>", methods=["GET"])
def check_job_id(job_id):
    sql = "SELECT id FROM vagas WHERE id = %s"
    job = (job_id,)
    mycursor.execute(sql, job)
    myresult = mycursor.fetchall()
    if (len(myresult) < 1):
       return 'Código da vaga não existe. Por favor, verfique e informe novamente.'
    else:
       return 'Código da vaga existe. Por favor, prossiga.'

@app.route("/job_messages/<user_id>", methods=["GET"])
def get_job_messages(user_id):
    sql = "SELECT pe.id_usuario, nome, email, formacao, tecnologias, experiencia_area, ingles, python FROM perguntas_obrigatorias po JOIN perguntas_eliminatorias pe ON pe.id_usuario = po.id_usuario WHERE po.id_usuario = %s"
    user = (user_id,)
    mycursor.execute(sql, user)
    myresult = mycursor.fetchall()
    if (len(myresult) < 1):
       return 'Usuário inexistente.'
    else:
        mydict = {
            "id": myresult[0][0],
            "nome": myresult[0][1],
            "email": myresult[0][2],
            "formacao": myresult[0][3],
            "tecnologias": myresult[0][4],
            "experiencia_area": myresult[0][5],
            "ingles": myresult[0][6],
            "python": myresult[0][7],
        }
        return mydict

@app.route("/job_application", methods=["POST"])
def job_application():
    application = json.loads(request.data)
    nome = application["nome"]
    email = application["email"]
    formacao = application["formacao"]
    tecnologias = application["tecnologias"]
    experiencia_area = application["experiencia_area"]
    ingles = application["ingles"]
    python = application["python"]

    #também é bom tratar os dados para garantir que string é string e booleano é booleano

    perguntas_obrigatorias = (nome,email,formacao,tecnologias)
    sql1 = "INSERT INTO perguntas_obrigatorias(nome, email, formacao, tecnologias) VALUES (%s, %s, %s, %s);"
    mycursor.execute(sql1, perguntas_obrigatorias)
    mydb.commit()

    perguntas_eliminatorias = (experiencia_area,ingles,python)
    sql2 = "INSERT INTO perguntas_eliminatorias(experiencia_area, ingles, python) VALUES (%s, %s, %s);"
    mycursor.execute(sql2, perguntas_eliminatorias)
    mydb.commit()

    returnstr = "Usuário " + nome + " inserido com sucesso!"
    return returnstr

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)