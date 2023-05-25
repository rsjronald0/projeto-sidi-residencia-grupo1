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

@app.route("/job_messages", methods=["GET"])
# Exemplo de envio de requisição de GET Job Messages:
# 127.0.0.1:5001/job_messages?user_id=5 (retorna os resultados para o usuário de ID 5)
# Retorna um dicionário com um campo "resp" contendo um array de todas as respostas dadas pelo usuário fornecido na URL da requisição
# Retorna um dicionário com campo "resp" False se o usuário não existe ou nunca respondeu nenhuma pergunta
def get_job_messages():
    user_id = int(request.args.get('user_id'))
    sql = "SELECT id_usuario, p.id_vaga, pergunta, resposta, tipo FROM respostas r JOIN perguntas p ON r.id_pergunta = p.id_pergunta WHERE id_usuario = %s AND p.id_vaga = (SELECT max(id_vaga) FROM respostas WHERE id_usuario = %s) ORDER BY p.id_pergunta ASC;"
    user = (user_id,user_id,)
    mycursor.execute(sql, user)
    myresult = mycursor.fetchall()
    if (len(myresult) < 1):
      data = {
         "resp": False
      }
      response = jsonify(data)
      response.headers['Access-Control-Allow-Origin'] = '*'
      return response
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
        response = jsonify(dictresp)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    
# API rodando localmente na porta 5001
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)