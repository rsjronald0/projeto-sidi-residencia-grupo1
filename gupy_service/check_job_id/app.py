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


@app.route("/check", methods=["GET"])
# Exemplo de envio de requisição de GET Check Job Id:
# 127.0.0.1:5002/check?job_id=5 (retorna o resultado para a vaga de ID 5)
# Retorna um dicionário com campo "resp" True se a vaga for válida ou existir
# Retorna um dicionário com campo "resp" False se a vaga não for válida ou não existir
def check_job_id():
    sql = "SELECT id_vaga FROM vagas WHERE id_vaga = %s"
    job_id = int(request.args.get('job_id'))
    job = (job_id,)
    mycursor.execute(sql, job)
    myresult = mycursor.fetchall()
    if (len(myresult) < 1):
      data = {
         'resp': False
      }
      response = jsonify(data)
      response.headers['Access-Control-Allow-Origin'] = '*'
      return response
    else:
      data = {
         'resp': True
      }
      response = jsonify(data)
      response.headers['Access-Control-Allow-Origin'] = '*'
      return response
    
# API rodando localmente na porta 5002
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)