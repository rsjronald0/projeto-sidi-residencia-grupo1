# Grupo 1 -> Projeto Chatbot
Utilizando Python com Flask e MySQL como banco de dados, esse projeto busca entregar para a empresa SiDi uma API que será integrada a um Chatbot com o propósito de facilitar o processo como um todo de contratação de indíviduos, como o envio de informações pertinentes à contratação e uma melhor visualização dos dados por parte da equipe de gestão de pessoas.

A API roda localmente na porta 5000 assim que você executar o arquivo app.py de algum dos microsserviços específico. Assim que executado, será criada a base de dados para aquele determinado serviço, juntamente com suas tabelas. Caso essa base de dados ou tabelas já existam localmente, não irá tentar gerá-las novamente.

Até o momento, a API possui 3 rotas no microsserviço "gupy_service":

/check/job_id -> job_id é um parâmetro que precisa ser preenchido na URL, exemplo: "127.0.0.1:5000/check/123". Nessa rota, será verificado se o id 123 existe na tabela de vagas.

/job_messages/user_id -> user_id é um parâmetro que precisa ser preenchido na URL, exemplo: "127.0.0.1:5000/job_messages/10". Nessa rota, todas as informações sobre o usuário com id 10 serão exibidas, que no caso são os dados e perguntas preenchidos pelo candidato ao se inscrever numa vaga.

/job_application -> Os dados de perguntas preenchidas pelo usuário são enviados através de um JSON numa requisição POST nessa rota. Nesse JSON, os seguintes campos foram considerados: "nome" (string), "email" (string), "formacao" (string), "tecnologias" (string), "experiencia_area" (boolean), "ingles" (boolean), "python" (boolean). Após o envio dessa requisição, os dados desse usuário específico são inseridos na base de dados MySQL local.
