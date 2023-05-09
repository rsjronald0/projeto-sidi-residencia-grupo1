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

@app.route("/job_questions", methods=["GET"])
# Exemplo de envio de requisição de GET Job Messages:
# 127.0.0.1:5003/job_questions?job_id=5 (retorna os resultados para a vaga de ID 5)
# Retorna um dicionário com um campo "resp" contendo um array de todas as perguntas da vaga fornecida na URL da requisição
# Retorna um dicionário com campo "resp" False se a vaga não existe
def get_job_messages():
    job_id = int(request.args.get('job_id'))
    sql = "SELECT pergunta, tipo FROM perguntas WHERE id_vaga = %s ORDER BY id_pergunta ASC;"
    job = (job_id,)
    mycursor.execute(sql, job)
    myresult = mycursor.fetchall()
    if (len(myresult) < 1):
      return { "resp" : False }
    else:
        myarray = []
        for m in myresult:
           mydict = {
              "pergunta": myresult[myresult.index(m)][0],
              "tipo": myresult[myresult.index(m)][1],
           }
           myarray.append(mydict)
        dictresp = {
           "resp": myarray
        }
        return dictresp
    
# API rodando localmente na porta 5003
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)