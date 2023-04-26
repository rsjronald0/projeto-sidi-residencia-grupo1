import json
from flask import Flask, request
import mysql.connector

app = Flask(__name__)

#Conexão com o banco de dados específico do serviço
mydb = mysql.connector.connect(
  host="localhost",
  user="sidi",
  password="sidi",
  database="gupy_service"
)

mycursor = mydb.cursor()

@app.route("/check/<job_id>", methods=["GET"])
# Exemplo de envio de requisição de GET Check Job Id:
# 127.0.0.1:5000/check/5 (retorna o resultado para a vaga de ID 5)
# Retorna a string "True" se a vaga for válida ou existir
# Retorna a string "False" se a vaga não for válida ou não existir
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
# Exemplo de envio de requisição de GET Job Messages:
# 127.0.0.1:5000/job_messages/5 (retorna os resultados para o usuário de ID 5)
# Retorna um dicionário com um campo "resp" contendo um array de todas as respostas dadas pelo usuário fornecido na URL da requisição
# Retorna a string "False" se o usuário não existe ou nunca respondeu nenhuma pergunta
def get_job_messages(user_id):
    sql = "SELECT id_usuario, r.id_vaga, pergunta, resposta, tipo FROM respostas r JOIN perguntas p ON r.id_pergunta = p.id_pergunta WHERE id_usuario = %s"
    user = (user_id,)
    mycursor.execute(sql, user)
    myresult = mycursor.fetchall()
    if (len(myresult) < 1):
       return 'False'
    else:
        myarray = []
        for m in myresult:
           mydict = {
              "id_usuario": myresult[myresult.index(m)][0],
              "id_vaga": myresult[myresult.index(m)][1],
              "pergunta": myresult[myresult.index(m)][2],
              "resposta": myresult[myresult.index(m)][3],
              "tipo": myresult[myresult.index(m)][4],
           }
           myarray.append(mydict)
        dictresp = {
           "resp": myarray
        }
        return dictresp

@app.route("/job_application", methods=["POST"])
# Exemplo de envio de requisição de POST Job Application:
# {
#    "id_vaga": 1,
#    "resposta1": "True",
#    "resposta2": "False",
#    "resposta3": "True",
#    "reposta4": "Lorem ipsum",
#    "resposta5": "teste@teste.com"
# }
# Retorna uma string "Respostas inseridas com sucesso" após a inserção dos dados
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

# API rodando localmente na porta 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)