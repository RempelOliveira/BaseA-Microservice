# Microservices Repo

Solução dividida em três microserviços com a finalidade de armazenar e disponibilzar dados relacionados a um ou mais CPFs.

Cada serviço é responsável por armazenar e disponibilizar dados e recursos específicos.

# Base A

Serviço responsável por armazenar e disponibilizar dados pessoais e dívidas relacionadas a um ou mais CPFs.

# Base B

Serviço responsável por armazenar dados pessoais adicionais relacionados a um ou mais CPFs. Sua funcionalidade principal é calcular e disponibilizar a pontuação relacionada a um determinado CPF com base em seu padrão financeiro. Esta pontuação é usada para referência em linhas de crédito, abertura de contas em bancos e outros fins.

# Base C

Serviço responsável por armazenar e disponibilizar o histórico de transações realizadas por um ou mais CPFs.

# Postman

Para utilizar os serviços sem a implementação de uma aplicação front-end, é necessário executar as rotas disponíveis via curl ou algum software de terceiros. Uma cópia da collection contendo exemplos de execução para uso no **Postman** pode ser importada através do arquivo ```postman-services-collection.js```.

# Principais Tecnologias Utilizadas

- [Python](https://www.python.org)
- [Postgres](https://www.postgresql.org)
- [MongoDB](https://www.mongodb.com)
- [Redis](https://redis.io)
- [Docker](https://www.docker.com)
- [Postman]()

# Melhorias

- Implementar ErrorHandler para tratamento de erros.
- Implementar CI/CD
