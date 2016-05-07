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


## Alguns detalhes de implementação

O servidor foi codificado em Python+Flask. Os dados são persistidos em uma base MySQL. O enunciado do problema não detalha sobre o nível de escalabilidade e disponibilidade exigidos, então fiz algo que começa simples mas pode ser estendido se necessário. Pode-se argumentar que SQLite poderia ser usado, mas isso não traria mais simplicidade ao código e escalar seria mais complicado.

Os testes foram implementados usando unittest.



## 

### Kubernetes

O serviço pode ser instalado em um cluster de containeres administrado por Kubernetes usando os seguinte comandos:

```sh
$ git@github.com:enyamada/deployment-time.git
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

Todas as configurações foram testadas em um cluster hospedado no google cloud.

