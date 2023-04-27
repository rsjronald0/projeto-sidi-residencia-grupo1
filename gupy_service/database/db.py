import mysql.connector

db_exists = False
vagas_exists = False
perguntas_exists = False
respostas_exists = False

# Conecta ao banco de dados MySQL local
mydb = mysql.connector.connect(
  host="localhost",
  user="sidi",
  password="sidi"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

# Verifica se a database gupy_service já existe, se não existe então é criada
for m in mycursor:
    for v in m:
        if (v == 'gupy_service'):
            db_exists = True

if (db_exists == False):
  mycursor.execute("CREATE DATABASE gupy_service")

# Conecta à database gupy_service após garantir sua existência
mydb = mysql.connector.connect(
  host="localhost",
  user="sidi",
  password="sidi",
  database="gupy_service"
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

# Checa a existências das tabelas "vagas", "perguntas" e "respostas", caso não existam então são criadas
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
  mycursor.execute("CREATE TABLE perguntas (id_pergunta INT PRIMARY KEY, id_vaga INT NOT NULL, pergunta VARCHAR(350), tipo ENUM('obrigatoria', 'eliminatoria'), FOREIGN KEY (id_vaga) REFERENCES vagas(id_vaga))")

if (respostas_exists == False):
  mycursor.execute("CREATE TABLE respostas (id_usuario INT NOT NULL, id_vaga INT NOT NULL, id_pergunta INT NOT NULL, resposta VARCHAR(350), FOREIGN KEY (id_vaga) REFERENCES vagas(id_vaga), FOREIGN KEY (id_pergunta) REFERENCES perguntas(id_pergunta))")