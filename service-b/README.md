# Base B

Serviço disponível para aplicações externas.

Este serviço é independente, ou seja, não precisa que os serviços **Base A** ou **Base B** sejam inicializados.

# Banco de Dados

Para fins de armazenamento e consulta, o banco de dados utilizado por este serviço é o **MongoDB**. Ao instalar a aplicação, o banco é criado e populado com dados fictícios.

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

Ao final da inicialização, o serviço estará disponível no seguinte endereço e porta ```http://localhost:5001```

# Rotas

- GET v1/users/:cpf/score

Rota disponível para exibição da pontuação do portador do CPF solicitado. Esta pontuação é calculada com base no histórico financeiro, idade e outros dados previamente cadastrados.

Header Necessário:

```
Api-Key: <:string>
```
