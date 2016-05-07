# Tempo de deployment

Esta é uma solução para o problema de cálculo de duração de deployments como proposto pela Elo7.

## A API

A Rest API implementada gira em torno de _steps_ (fases) de deployment, por isso esse é o nome do recurso central. As chamadas possíveis são:
  - `POST /v1/steps?component=xx&version=yy&owner=zz&status=ww`: Esta chama registra dados sobre uma determinada fase do deployment. Os parâmetros (todos obrigatórios) são:
    - component: nome do componente em deployment
    - version: versão 
    - owner: id do engenheiro reponsável
    - status: status
  - `GET /v1/steps?par1=v1&par2=v2...`: Obtém lista de fases registradas. Alguns parâmetros (todos opcionais) podem ser usados para filtragem:
    - start_datatetime: restringe a busca à apenas fases que começaram depois da data/hora declarada. O formato esperado é AAAA-MM-DD hh:mm:ss, e sempre será interpretado como UTC. 
    - end_datetime: considera apenas fases que terminaram até a data/hora especificada.
    - component: componente desejado
    - owner: responsável.
    - format: Define o formado de saída. São suportados csv (default) ou json.



## Como executar

O serviço foi "dockerizado" e o ambiente ideal para execução seria em um cluster (como o Swarm, AWS ECS, Kubernetes etc). 

Entendo (sem absoluta certeza) que a Elo7 adota o Kubernetes, e foi então essa a principal solução que estudei. Além disso, fiz uma versão mais simplificada (e que não depende de um cluster já existente) que usa um script para criar uma instância AWS EC2 com os contêineres já prontos em alguns minutos. Abaixo descrevo as opções.

### Usando AWS

A partir de uma máquina com o docker engine instalado, basta chamar

```sh
sudo docker run -it -e AWS_ACCESS_KEY_ID=XXX -e AWS_KEY_NAME=my-key-name -e AWS_SECRET_ACCESS_KEY=YYYY  enyamada/steps-launcher:1.0
```

Em segundos o script deve imprimir o nome do servidor criado junto com alguns exemplos de execução. 

#### Alguns detalhes 

Basicamente criamos uma instância EC2 e então, usado docker-compose, instanciamos dois contêineres: enyamada/steps-db (que é um MySQL com as bases de dados) e enyamada/steps-fe (o frontend).



### Usando Kubernetes

O serviço pode ser instalado em um cluster de containeres administrado por Kubernetes usando os seguinte comandos:

```sh
$ git clone git@github.com:enyamada/deployment-time.git
$ cd deployment-time
$ kubectl -f kubernetes/
```

O instanciamento dos pods pode demorar um pouco (em especial, porque as imagens estão no repositório público do docker e, portanto,. precisam ser baixadas de lá). A configuração prevê a criação de duas instâncias de pods de front end (_steps-fe_) e uma de banco de dados (_steps-db_).

Quando a saída do comando `kubectl get pods -l app=steps-api` indicar que os 3 pods estão com status de _Running_ (como abaixo) então o serviço estará pronto.

```sh
NAME                        READY     STATUS    RESTARTS   AGE
steps-db-2391806042-rxf6u   1/1       Running   0          53s
steps-fe-3824271607-l2m6v   1/1       Running   0          52s
steps-fe-3824271607-qurjj   1/1       Running   0          52s
```

Kubernetes deve alocar um endereço IP externo para o serviço _steps-fe_. Para descobrir qual é, um possível comando é `kubectl get service steps-fe -o go-template={{.spec.clusterIP}}`.

Finalmente, de posse do endereço IP, podemos fazer as chamadas usando comandos como ` curl -X POST 'ENDERECO-IP/v1/steps?component=c1&version=v1&owner=o1&status=s1'`

Obviamente, tudo isso pode ser trivialmente automatizado num shell script.

Para testar, usei um cluster hospedado no google cloud.



## Alguns detalhes de implementação

O servidor foi codificado em Python+Flask. Os dados são persistidos em uma base MySQL. O enunciado do problema não detalha sobre o nível de escalabilidade e disponibilidade exigidos, então fiz algo que começa simples mas pode ser estendido se necessário. Pode-se argumentar que SQLite poderia ser usado, mas isso não traria mais simplicidade ao código (seria praticamente idêntico) e escalar seria mais complicado.

Os testes foram implementados usando unittest.

### O que não foi feito (mas poderia/deveria ser feito nas iterações seguintes)

* Segurança: nenhum tipo de autenticação ou autorização foi implementado. Na mesma linha, os dados submetidos pelo usuário não são "sanitizados".
* 
