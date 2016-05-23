# Teste Engenheiro de Software/DevOps Elo7

Como parte do processo seletivo do Elo7, gostaríamos que você fizesse uma pequena tarefa. O problema proposto é uma situação fictícia e você não estará desenvolvendo uma solução para nossa empresa neste teste. Conforme seu resultado daremos continuidade ao processo te convidando para uma sessão de pair-programming.
 
Durante o desenvolvimento da aplicação você pode usar a linguagem de sua preferência.

O objetivo dessa tarefa é podermos analisar o desenvolvimento e a entrega de uma aplicação simples em um ambiente o mais próximo possível de produção. Vamos avaliar o código gerado, como sua aplicação será executada e como você preparou o ambiente para que ela possa executar.O último item é muito importante e terá um peso considerável na avaliação.

A execução da aplicação deverá ser realizada dentro de um container, preferêncialmente Docker. Os fontes da aplicação, os scripts e arquivos de configuração, se você os utilizar, criados para a execução da aplicação e do container deverão ser versionados para avaliação.Também deve ser versionado um arquivo README com instruções para a execução de seu projeto.

Se você utilizar alguma ferramenta para geração ou depuração do container versione essas configurações também.
 
Crie um projeto no seu Github para que vejamos os passos feitos através dos commits para resolver a tarefa.

Sinta-se à vontade para criar em cima do problema abaixo. Caso algo não esteja claro, pode assumir o que seja mais claro para você e indique suas suposições em documentação. A especificação é bem básica e, portanto, caso deseje evoluir a ideia seguindo essa base, fique à vontade: por exemplo, utilizar composição de containers, usar ferramentas para facilitar a geração da imagem do container, etc.

Qualquer dúvida maior pode nos perguntar, mas no geral, divirta-se!

# Quanto tempo demora um deploy?

Nosso time de engenharia realiza várias entregas diariamente em produção e o tempo de cada deploy pode variar.

Em uma de nossas retrospectivas um membro do time citou que o tempo de deploy estava aumentando ao longo dos sprints, mas não sabia precisar qual era essa taxa de crescimento.

Como ação da retrospectiva surgiu a iniciativa de que fosse desenvolvida alguma solução automática e confiável que pudesse medir o tempo gasto em cada etapa de cada processo de deploy. 

Ficou decidido que uma solução simples e que seria facilmente integrada com nosso fluxo de entregas seria o desenvolvimento de uma API que recebesse uma requisição HTTP e salvasse os parâmetros para que eles pudessem ser analizados posteriormente.

Portanto convidamos-o para nos auxiliar com resolução do nosso problema como seu desafio técnico.

Você deverá desenvolver uma aplicação simples que receba uma requisição HTTP com os seguintes parâmetros: 
* **Componente**: Componente que está em processo de deploy
* **Versão**: Versão que está sendo entregue
* **Responsável**: Nome do membro do time de engenharia que está realizando o processo de deploy
* **Status**: Status do processo de deploy

Sua aplicação deverá persistir todos os dados recebidos e o horário que a chamada foi recebida, ou seja, sua aplicação deverá salvar as seguintes informações:
* **Componente**: Componente que está em processo de deploy
* **Versão**: Versão que está sendo entregue
* **Responsável**: Nome do membro do time de engenharia que está realizando o processo de deploy
* **Status**: Status do processo de deploy
* **Data**: data com horário que a chamada foi recebida

Os dados devem ser salvos da maneira e no formato que preferir, de forma que não agregue complexidade desnecessária na sua solução ou que o impeça de completar sua tarefa, porém é importante que nenhum dado seja perdido.

Embora não faça parte do desafio recuperar ou retornar os dados recebidos é importante que os dados sejam salvos de forma que a recuperação ou o export destes dados para uma planilha seja simples e rápido.
