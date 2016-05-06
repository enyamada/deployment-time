# deployment-time



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

