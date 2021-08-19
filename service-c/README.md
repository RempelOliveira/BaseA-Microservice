# Base C

Serviço disponível para aplicações externas.

Este serviço não é totalmente independente, porém, irá operar com consultas normalmente caso o serviço **Base A** não esteja inicializado. O serviço **Base A** é responsável pelo cadastro do histórico neste serviço.

# Banco de Dados

Para fins de armazenamento e consulta, o banco de dados utilizado por este serviço é o **MongoDB**. Para fins de perfomance em determinadas rotas, foi implementado o uso de **Redis**. Ao instalar a aplicação, os bancos são criados e populados com dados fictícios.

# Instalação

É necessário que o ambiente escolhido para instalação possua o **Docker** e todas suas dependências previamente instaladas, uma vez instalado, basta seguir os seguintes passos:

Para instalar a aplicação, basta rodar o comando abaixo.

```
$ make install
```

O comando **make install** é responsável pela execução de todas as pendências do serviço, ao final, testes automatizados serão executados.

Caso seja necessário executar comandos individualmente, basta utilizar o comando ```make <option>```.

Para exibir a lista de comandos disponníveis, basta executar o comando ```make```.

# Inicialização

Para inicializar o serviço, basta executar o comando abaixo.

```
$ make run
```

Ao final da inicialização, o serviço estará disponível no seguinte endereço e porta ```http://localhost:5002```

# Rotas

- GET v1/users/:cpf/last_query

Rota disponível para exibição da última consulta das dívidas financeiras do portador do CPF solicitado.

Header Necessário:

```
Api-Key: <:string>
```

- GET v1/users/<cpf:string>/last_credit_card_purchase

Rota disponível para exibição da última compra com cartão de crédito do portador do CPF solicitado.

Header Necessário:

```
Api-Key: <:string>
```

- GET v1/users/<cpf:string>/financial_transactions

Rota paginada disponível para exibição de todas as movimentações financeiras realizadas pelo portador do CPF solicitado.

Parâmetros Disponíveis:

```
page: <:int>
per_page: <:int>
```

Header Necessário:

```
Api-Key: <:string>
```
