# Grupo 1 -> Projeto Chatbot
Utilizando Python com Flask e MySQL como banco de dados, esse projeto busca entregar para a empresa SiDi uma API que será integrada a um Chatbot com o propósito de facilitar o processo como um todo de contratação de indíviduos, como o envio de informações pertinentes à contratação e uma melhor visualização dos dados por parte da equipe de gestão de pessoas.

A API roda localmente, com uma porta específica para cada serviço em execução.

Cada microsserviço conta com um arquivo app.py que representa a execução da API localmente, e com outro arquivo db.py, presente na pasta database que é responsável pela criação da database e tabelas do serviço MySQL localmente.

Até o momento, a API possui 3 rotas/serviços no microsserviço "gupy_service":

/check?job_id -> job_id é um parâmetro GET que precisa ser preenchido, exemplo: "127.0.0.1:5002/check?job_id=123". Nessa URL de exemplo, será verificado se o id 123 existe na tabela de vagas.

/job_messages?user_id -> user_id é um parâmetro GET que precisa ser preenchido, exemplo: "127.0.0.1:5001/job_messages?user_id=10". Nessa URL de exemplo, todas as informações sobre o usuário com id 10 serão exibidas, que no caso são todas as respostas das perguntas preenchidas pelo candidato ao se inscrever numa vaga.

/job_application -> Os dados de perguntas preenchidas pelo usuário são enviados através de um JSON numa requisição POST nessa rota. Nesse JSON, os seguintes campos foram considerados: "id_vaga" (int), "resposta1" (string), "resposta2" (string), etc. Ou seja, é necessário o envio de um campo chamado "id_vaga" ou somente "vaga" para fornecer o id da vaga em específico, e todos os outros campos enviados são considerados respostas, na sequência em que forem enviados na requisição, então a resposta1 deveria ser a resposta da pergunta com id 1 da determinada vaga na tabela de perguntas, e assim por diante. Não é necessário enviar user_id pois a API acessa o último id de usuário no banco de dados e colocará o usuário enviado como o próximo, logo depois do maior id. Após o envio dessa requisição, os dados desse usuário específico são inseridos na base de dados MySQL local.

A API possui 1 rota no microsserviço "sidi_service", a job_application, que tem a mesma função que a job_application do microsserviço da Gupy, porém é tudo enviado para uma outra database, chamada de sidi_service, criada no respectivo db.py.
