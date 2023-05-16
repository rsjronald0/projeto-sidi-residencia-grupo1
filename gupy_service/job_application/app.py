import json
from flask import Flask, request, jsonify
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

    data = {
       "resp": "Respostas inseridas com sucesso"
    }
    response = jsonify(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# API rodando localmente na porta 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)