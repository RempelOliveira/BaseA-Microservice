# Base A

Serviço disponível para portadores de CPF pré-cadastrados.

Este serviço é independente, porém, para que o serviço **Base C** registre o histórico de consultas do usuário, ambos precisam ser inicializados, isso porque, este serviço envia informações em background para o serviço **Base C**.

# Banco de Dados

Para fins de armazenamento e consulta, o banco de dados utilizado por este serviço é o **PostgreSQL**. Ao instalar a aplicação, o banco é criado e populado com dados fictícios.

# Instalação

É necessário que o ambiente escolhido para instalação possua o **Docker** e todas suas dependências previamente instaladas, uma vez instalado, basta seguir os passos abaixo.

Para instalar a aplicação, basta rodar o comando:

```
$ make install
```

O comando **make install** é responsável pela execução de todas as pendências do serviço, ao final, testes automatizados serão executados.

Caso seja necessário executar comandos individualmente, basta utilizar o comando ```make <option>```

Para exibir a lista de comandos disponníveis, basta executar o comando ```make```

# Inicialização

Para inicializar o serviço, basta executar o comando abaixo.

```
$ make run
```

Ao final da inicialização, o serviço estará disponível no seguinte endereço e porta ```http://localhost:5000```

# Rotas

- POST v1/users/login

Rota disponível para autenticação de usuários portadores de CPF pré-cadastrados no serviço.

Dados de entrada:

```
{
    "cpf": <:string>,
    "password": <:string>
}
```

Uma vez em que o login é bem sucedido, o serviço retornará um **Bearer Token** para ser utilizado nas demais rotas.

- DELETE v2/users/logout

Rota disponível para desautenticação de usuários que geraram um **Bearer Token** na rota de autenticação. O token passado é armazenado em banco de dados para fins de validação, uma vez desautenticado, o token é considerado inválido para novas autenticações.

Header Necessário:

```
Authorization: Bearer <:string>
```

- GET v1/users/account

Rota disponível para exibição dos dados do usuário autenticado.

Header Necessário:

```
Authorization: Bearer <:string>
```

- GET v1/users/debts

Rota paginada disponível para exibição das dívidas financeiras do usuário autenticado.

Parâmetros Disponíveis:

```
page: <:int>
per_page: <:int>
```

Header Necessário:

```
Authorization: Bearer <:string>
```
